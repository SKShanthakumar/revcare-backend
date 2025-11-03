from fastapi import HTTPException
from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession as Session
from sqlalchemy.orm import selectinload
from sqlalchemy.exc import IntegrityError
from typing import List
from app.models import Service, PriceChart, FuelType
from app.schemas import ServiceUpdate, ServiceUpdateWithForeignData
from app.utilities.data_processing import filter_data_for_model
from app.services import crud

# utils
async def update_service_price_chart(db: Session, service_id: int, new_price_chart_data: list):
    """
    Update the price chart for a given service.
    Handles add, update, and delete logic.
    """

    # Step 1: Fetch existing price chart records for the service
    result = await db.execute(
        select(PriceChart).where(PriceChart.service_id == service_id)
    )
    existing_price_charts = result.scalars().all()

    # Convert to dict for faster lookup
    existing_map = {pc.car_class_id: pc for pc in existing_price_charts}
    new_map = {p.car_class_id: p for p in new_price_chart_data}

    # Step 2: Update or add entries
    for car_class_id, new_pc in new_map.items():
        if car_class_id in existing_map:
            # Update price if different
            existing_pc = existing_map[car_class_id]
            if existing_pc.price != new_pc.price:
                existing_pc.price = new_pc.price
        else:
            # Add new entry
            new_entry = PriceChart(
                service_id=service_id,
                car_class_id=car_class_id,
                price=new_pc.price
            )
            db.add(new_entry)

    # Step 3: Bulk delete removed entries
    removed_ids = set(existing_map.keys()) - set(new_map.keys())
    if removed_ids:
        await db.execute(
            delete(PriceChart).where(
                PriceChart.service_id == service_id,
                PriceChart.car_class_id.in_(removed_ids),
            )
        )

    # db not committed caller function should commit

async def get_fuel_type_models(db: Session, fuel_ids: List[int]):
    if not fuel_ids:
        return []

    result = await db.execute(
        select(FuelType).where(FuelType.id.in_(fuel_ids))
    )
    return result.scalars().all()


# business logic
async def create_service(db: Session, data: dict):
    # check customer trying to access other customer's address - if condition also bypasses admin
    filtered_data = filter_data_for_model(Service, data)
    service = Service(**filtered_data)
    db.add(service)

    try:
        # just flush to get service.id without full commit
        await db.flush()
        await db.refresh(service)

    except IntegrityError:
        await db.rollback()
        raise HTTPException(status_code=400, detail="Invalid foreign key reference")

    # fetch fuel type models from db
    service.fuel_types = await get_fuel_type_models(db, data.get("fuel_type_ids", []))

    # add price chart
    if "price_chart" in data and data["price_chart"]:
        price_chart_models = [
            PriceChart(
                service_id=service.id,
                car_class_id=item["car_class_id"],
                price=item["price"],
            )
            for item in data["price_chart"]
        ]
        service.price_chart = price_chart_models
        db.add_all(price_chart_models)

    await db.commit()

    # re fetch from db with eager loading
    service = await crud.get_one_record(
        db=db,
        model=Service,
        filters={"id": service.id},
        options=[
            selectinload(Service.category),
            selectinload(Service.price_chart).selectinload(PriceChart.car_class),
            selectinload(Service.fuel_types),
        ]
    )
    return service


async def update_service(db: Session, service_id: int, update_schema: ServiceUpdateWithForeignData):
    service_base_schema = ServiceUpdate(**update_schema.model_dump(exclude_none=True))
    new_data = service_base_schema.model_dump(exclude_none=True)

    flag = False    # to check any db transaction made
    
    if new_data:
        flag = True
        await crud.update_record_by_primary_key(db, service_id, new_data, Service)

    service: Service = await crud.get_record_by_primary_key(db, service_id, Service)

    if update_schema.price_chart:
        flag = True
        await update_service_price_chart(db, service_id, update_schema.price_chart)

    if update_schema.fuel_type_ids:
        flag = True
        fuel_types = await get_fuel_type_models(db, update_schema.fuel_type_ids)
        service.fuel_types = fuel_types

    if flag:
        await db.commit()
    await db.refresh(service)

    return service