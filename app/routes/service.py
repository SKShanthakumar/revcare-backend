from fastapi import APIRouter, Depends, Security, HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession as Session
from typing import List, Optional
from app.database.dependencies import get_postgres_db
from app.models import ServiceCategory, Service, ServiceReview
from app.schemas import ServiceCategoryCreate, ServiceCategoryResponse, ServiceCategoryUpdate, ServiceCreate, ServiceResponse, ServiceUpdateWithForeignData, ServiceReviewCreate, ServiceReviewResponse, ServiceReviewUpdate
from app.services import crud, service as car_service
from app.auth.dependencies import validate_token

router = APIRouter()

# category routes
@router.get("/category", response_model=List[ServiceCategoryResponse])
async def get_categories(db: Session = Depends(get_postgres_db), payload = Security(validate_token, scopes=["READ:SERVICE_CATEGORIES"])):
    return await crud.get_all_records(db, ServiceCategory)

@router.post("/category", response_model=ServiceCategoryResponse)
async def create_category(category: ServiceCategoryCreate, db: Session = Depends(get_postgres_db), payload = Security(validate_token, scopes=["WRITE:SERVICE_CATEGORIES"])):
    return await crud.create_record(db, category.model_dump(), ServiceCategory)

@router.put("/category/{id}", response_model=ServiceCategoryResponse)
async def update_category_by_id(id: int, category: ServiceCategoryUpdate, db: Session = Depends(get_postgres_db), payload = Security(validate_token, scopes=["UPDATE:SERVICE_CATEGORIES"])):
    return await crud.update_record_by_primary_key(db, id, category.model_dump(exclude_none=True), ServiceCategory)

@router.delete("/category/{id}", response_class=JSONResponse)
async def delete_category_by_id(id: int, db: Session = Depends(get_postgres_db), payload = Security(validate_token, scopes=["DELETE:SERVICE_CATEGORIES"])):
    message = await crud.delete_record_by_primary_key(db, id, ServiceCategory)
    return JSONResponse(content=message)


# service review routes
@router.get("/review/{service_id}", response_model=List[ServiceReviewResponse])
async def get_reviews_for_service(service_id: int, db: Session = Depends(get_postgres_db), payload = Security(validate_token, scopes=["READ:SERVICE_REVIEWS"])):
    return await crud.get_all_records(db, ServiceReview, filters={"service_id": service_id})

@router.post("/review", response_model=ServiceReviewResponse)
async def create_review(review: ServiceReviewCreate, db: Session = Depends(get_postgres_db), payload = Security(validate_token, scopes=["WRITE:SERVICE_REVIEWS"])):
    customer_id = payload.get("user_id")
    if not customer_id.startswith("CST"):
        raise HTTPException(status_code=403, detail="Operation not permitted. Only Customers can add reviews")
    
    data = review.model_dump()
    data["customer_id"] = customer_id
    return await crud.create_record(db, data, ServiceReview)

@router.put("/review/{service_id}", response_model=ServiceReviewResponse)
async def update_review_by_id(service_id: int, review: ServiceReviewUpdate, db: Session = Depends(get_postgres_db), payload = Security(validate_token, scopes=["UPDATE:SERVICE_REVIEWS"])):
    customer_id = payload.get("user_id")
    if not customer_id.startswith("CST"):
        raise HTTPException(status_code=403, detail="Operation not permitted. Only Customers can update reviews")
    
    # build composite primary key
    pk = {
        "customer_id": customer_id,
        "service_id": service_id
    }
    return await crud.update_record_by_composite_key(db, pk, review.model_dump(exclude_none=True), ServiceReview)

@router.delete("/review/{service_id}", response_class=JSONResponse)
async def delete_review_by_id(service_id: int, db: Session = Depends(get_postgres_db), payload = Security(validate_token, scopes=["DELETE:SERVICE_REVIEWS"])):
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


# service routes
@router.get("/", response_model=List[ServiceResponse])
async def get_services_by_category_id(category_id: Optional[int] = None, db: Session = Depends(get_postgres_db), payload = Security(validate_token, scopes=["READ:SERVICES", "READ:PRICE_CHART"])):
    filters = {"category_id": category_id} if category_id else None
    return await crud.get_all_records(db, Service, filters=filters)

@router.post("/", response_model=ServiceResponse)
async def create_service(service: ServiceCreate, db: Session = Depends(get_postgres_db), payload = Security(validate_token, scopes=["WRITE:SERVICES", "WRITE:PRICE_CHART"])):
    return await car_service.create_service(db, service.model_dump())

@router.put("/{id}", response_model=ServiceResponse)
async def update_service_by_id(id: int, service: ServiceUpdateWithForeignData, db: Session = Depends(get_postgres_db), payload = Security(validate_token, scopes=["UPDATE:SERVICES", "UPDATE:PRICE_CHART"])):
    return await car_service.update_service(db, id, service)

@router.delete("/{id}", response_class=JSONResponse)
async def delete_service_by_id(id: int, db: Session = Depends(get_postgres_db), payload = Security(validate_token, scopes=["DELETE:SERVICES", "DELETE:PRICE_CHART"])):
    message = await crud.delete_record_by_primary_key(db, id, Service)
    return JSONResponse(content=message)