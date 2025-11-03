from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession as Session
from sqlalchemy.orm import selectinload
from sqlalchemy.exc import IntegrityError
from app.models import Service, PriceChart, FuelType
from app.utilities.data_processing import filter_data_for_model

async def create_service(db: Session, data: dict):
    # check customer trying to access other customer's address - if condition also bypasses admin
    filtered_data = filter_data_for_model(Service, data)
    service = Service(**filtered_data)
    try:
        # add service to db 
        db.add(service)    
        await db.commit()
        await db.refresh(service)

    except IntegrityError:
        await db.rollback()
        raise HTTPException(status_code=400, detail="Invalid foreign key reference")

    # fetch fuel type models from db
    result = await db.execute(
        select(FuelType).where(FuelType.id.in_(data["fuel_type_ids"]))
    )
    fuel_types = result.scalars().all()
    service.fuel_types = fuel_types

    # add price chart
    price_chart_models = []
    for price_dict in data["price_chart"]:
        price_chart_model = PriceChart(service_id=service.id, car_class_id=price_dict["car_class_id"], price=price_dict["price"])
        price_chart_model.service = service
        price_chart_models.append(price_chart_model)
    db.add_all(price_chart_models)

    await db.commit()

    # re fetch from db with eager loading
    result = await db.execute(
        select(Service)
        .options(
            selectinload(Service.category),
            selectinload(Service.price_chart).selectinload(PriceChart.car_class),
            selectinload(Service.fuel_types)
        )
        .where(Service.id == service.id)
    )
    service = result.scalar_one()

    return service
