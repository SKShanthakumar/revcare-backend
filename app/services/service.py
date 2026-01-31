from fastapi import HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy import select, delete, func, cast
from sqlalchemy.ext.asyncio import AsyncSession as Session
from sqlalchemy.orm import selectinload
from sqlalchemy.exc import IntegrityError
from pgvector.sqlalchemy import Vector
from typing import List
from app.models import Service, PriceChart, FuelType, ServiceReview
from app.schemas import ServiceUpdate, ServiceUpdateWithForeignData, ServiceReviewCreate, ServiceReviewUpdate
from app.utilities.data_utils import filter_data_for_model
from app.services import crud, recommendation

# utils
async def update_service_price_chart(db: Session, service_id: int, new_price_chart_data: list):
    """
    Update the price chart for a given service.
    
    Handles add, update, and delete logic for price chart entries.
    Compares existing price charts with new data and performs necessary updates.
    Caller function should commit the transaction.
    
    Args:
        db: Async database session
        service_id: Service ID to update price chart for
        new_price_chart_data: List of price chart entries with car_class_id and price
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
    """
    Get fuel type model instances by IDs.
    
    Args:
        db: Async database session
        fuel_ids: List of fuel type IDs
        
    Returns:
        list: List of FuelType model instances
    """
    if not fuel_ids:
        return []

    result = await db.execute(
        select(FuelType).where(FuelType.id.in_(fuel_ids))
    )
    return result.scalars().all()

def serialize_price_chart(price_charts: List[PriceChart]):
    result = {}
    for price_chart in price_charts:
        result[price_chart.car_class_id] = float(price_chart.price)
    return result

def service_json(service: Service):
    return {
        'id': service.id,
        'title': service.title,
        'description': service.description,
        'works': service.works,
        'warranty_kms': service.warranty_kms,
        'warranty_months': service.warranty_months,
        'time_hrs': service.time_hrs,
        'difficulty': service.difficulty,
        'images': service.images,
        'price_chart': serialize_price_chart(service.price_chart),
        'fuel_types': [fuel_type.id for fuel_type in service.fuel_types],
    }

# business logic
async def create_service(db: Session, data: dict):
    """
    Create a new service with price chart and fuel types.
    
    Creates a service record, associates fuel types, and creates price chart entries.
    Returns the service with all related entities loaded.
    
    Args:
        db: Async database session
        data: Dictionary containing service data, fuel_type_ids, and price_chart
        
    Returns:
        Service: Created service instance with related entities loaded
        
    Raises:
        HTTPException: 400 if there's an integrity error (invalid foreign key reference)
    """
    # create text vector for recommendation system
    text = f"""
    Title: {data.title}
    Description: {data.description}
    Symptoms: {data.symptoms}
    """
    embedding = await recommendation.generate_embedding(text)
    print(embedding)
    data["embedding"] = embedding

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
    """
    Update a service including price chart and fuel types.
    
    Updates service fields, price chart, and fuel type associations.
    Can update any combination of service fields, price chart, or fuel types.
    
    Args:
        db: Async database session
        service_id: Service ID to update
        update_schema: Update schema with service fields, price_chart, and fuel_type_ids
        
    Returns:
        Service: Updated service instance (currently returns None, may need fix)
        
    Raises:
        HTTPException: 
            - 404 if service is not found
            - 400 if there's duplicate or invalid data
    """
    service_base_schema = ServiceUpdate(**update_schema.model_dump(exclude_none=True))
    new_data = service_base_schema.model_dump(exclude_none=True)

    service: Service = await crud.get_record_by_primary_key(db, service_id, Service)
    if not service:
        raise HTTPException(status_code=404, detail="Service not found")

    flag = False    # to check any db transaction made
    
    if new_data:
        flag = True
        if "symptoms" in new_data:
            # update embedding if symptoms changed
            text = f"""
            Title: {new_data.get('title', service.title)}
            Description: {new_data.get('description', service.description)}
            Symptoms: {new_data['symptoms']}
            """
            embedding = await recommendation.generate_embedding(text)
            print(embedding)
            new_data["embedding"] = embedding
            
        await crud.update_record_by_primary_key(db, service_id, new_data, Service)

    if update_schema.price_chart is not None:
        flag = True
        await update_service_price_chart(db, service_id, update_schema.price_chart)
        
    if update_schema.fuel_type_ids is not None:
        flag = True
        if len(update_schema.fuel_type_ids) > 0:
            fuel_types = await get_fuel_type_models(db, update_schema.fuel_type_ids)
            service.fuel_types = fuel_types
        else:
            service.fuel_types = []

    if flag:
        try:
            await db.commit()
        except IntegrityError:
            await db.rollback()
            raise HTTPException(status_code=400, detail="Duplicate or invalid data detected.")

    await db.refresh(service)

    return 


async def create_review(review: ServiceReviewCreate, db: Session, payload: dict):
    """
    Create a service review.
    
    Args:
        review: Service review creation data
        db: Async database session
        payload: Token payload containing user_id
        
    Returns:
        ServiceReview: Created review instance
        
    Raises:
        HTTPException: 403 if user is not a customer
    """
    customer_id = payload.get("user_id")
    if not customer_id.startswith("CST"):
        raise HTTPException(status_code=403, detail="Operation not permitted. Only Customers can add reviews")
    
    data = review.model_dump()
    data["customer_id"] = customer_id
    return await crud.create_record(db, data, ServiceReview)

async def update_review_by_id(service_id: int, review: ServiceReviewUpdate, db: Session, payload: dict):
    """
    Update a service review.
    
    Args:
        service_id: Service ID for the review
        review: Updated review data
        db: Async database session
        payload: Token payload containing user_id
        
    Returns:
        ServiceReview: Updated review instance
        
    Raises:
        HTTPException: 403 if user is not a customer
    """
    customer_id = payload.get("user_id")
    if not customer_id.startswith("CST"):
        raise HTTPException(status_code=403, detail="Operation not permitted. Only Customers can update reviews")
    
    # build composite primary key
    pk = {
        "customer_id": customer_id,
        "service_id": service_id
    }
    return await crud.update_record_by_composite_key(db, pk, review.model_dump(exclude_none=True), ServiceReview)

async def delete_review_by_id(service_id: int, db: Session, payload: dict):
    """
    Delete a service review.
    
    Args:
        service_id: Service ID for the review
        db: Async database session
        payload: Token payload containing user_id
        
    Returns:
        JSONResponse: Success message
        
    Raises:
        HTTPException: 403 if user is not a customer
    """
    customer_id = payload.get("user_id")
    if not customer_id.startswith("CST"):
        raise HTTPException(status_code=403, detail="Operation not permitted. Only Customers can delete reviews")
    
    # build composite primary key
    pk = {
        "customer_id": customer_id,
        "service_id": service_id
    }
    message = await crud.delete_record_by_composite_key(db, pk, ServiceReview)
    return JSONResponse(content=message)


async def recommend_service(query: str, db: Session):
    query_embedding = await recommendation.generate_embedding(query)

    VECTOR_DIM = 768
    similarity = (
        1 - func.cosine_distance(
            Service.embedding,
            cast(query_embedding, Vector(VECTOR_DIM))
        )
    )

    stmt = (
        select(
            Service,
            similarity.label("score")
        )
        .options(
            selectinload(Service.fuel_types),
            selectinload(Service.price_chart),
        )
        .order_by(
            func.cosine_distance(
                Service.embedding,
                cast(query_embedding, Vector(VECTOR_DIM))
            )
        )
        .limit(5)
    )

    rows = await db.execute(stmt)
    results = rows.all()

    result = [
        {**service_json(service), "score": round(float(score) * 100, 1)}
        for service, score in results
    ]
    return result


async def get_services_categorized(db: Session):
    services: List[Service] = await crud.get_all_records(db, Service)
    category_dict = {}

    for service in services:
        service_json = service_json(service)

        category_id = service.category.id
        if category_id in category_dict:
            category_dict[category_id]['services'].append(service_json)
        else:
            category_dict[category_id] = {
                'id': category_id,
                'category_name': service.category.name,
                'services': [service_json]
            }

    return category_dict.values()
