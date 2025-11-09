from fastapi import APIRouter, Depends, Security
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
    """
    Get all service categories.
    
    Args:
        db: Database session
        payload: Validated token payload
        
    Returns:
        List[ServiceCategoryResponse]: List of service categories
    """
    return await crud.get_all_records(db, ServiceCategory)

@router.post("/category", response_model=ServiceCategoryResponse)
async def create_category(category: ServiceCategoryCreate, db: Session = Depends(get_postgres_db), payload = Security(validate_token, scopes=["WRITE:SERVICE_CATEGORIES"])):
    """
    Create a new service category.
    
    Args:
        category: Service category creation data
        db: Database session
        payload: Validated token payload
        
    Returns:
        ServiceCategoryResponse: Created service category
    """
    return await crud.create_record(db, category.model_dump(), ServiceCategory)

@router.put("/category/{id}", response_model=ServiceCategoryResponse)
async def update_category_by_id(id: int, category: ServiceCategoryUpdate, db: Session = Depends(get_postgres_db), payload = Security(validate_token, scopes=["UPDATE:SERVICE_CATEGORIES"])):
    """
    Update a service category.
    
    Args:
        id: Service category ID
        category: Updated service category data
        db: Database session
        payload: Validated token payload
        
    Returns:
        ServiceCategoryResponse: Updated service category
    """
    return await crud.update_record_by_primary_key(db, id, category.model_dump(exclude_none=True), ServiceCategory)

@router.delete("/category/{id}", response_class=JSONResponse)
async def delete_category_by_id(id: int, db: Session = Depends(get_postgres_db), payload = Security(validate_token, scopes=["DELETE:SERVICE_CATEGORIES"])):
    """
    Delete a service category.
    
    Args:
        id: Service category ID
        db: Database session
        payload: Validated token payload
        
    Returns:
        JSONResponse: Success message
    """
    message = await crud.delete_record_by_primary_key(db, id, ServiceCategory)
    return JSONResponse(content=message)


# service review routes
@router.get("/review/{service_id}", response_model=List[ServiceReviewResponse])
async def get_reviews_for_service(service_id: int, db: Session = Depends(get_postgres_db), payload = Security(validate_token, scopes=["READ:SERVICE_REVIEWS"])):
    """
    Get all reviews for a service.
    
    Args:
        service_id: Service ID
        db: Database session
        payload: Validated token payload
        
    Returns:
        List[ServiceReviewResponse]: List of service reviews
    """
    return await crud.get_all_records(db, ServiceReview, filters={"service_id": service_id})

@router.post("/review", response_model=ServiceReviewResponse)
async def create_review(review: ServiceReviewCreate, db: Session = Depends(get_postgres_db), payload = Security(validate_token, scopes=["WRITE:SERVICE_REVIEWS"])):
    """
    Create a service review.
    
    Args:
        review: Service review creation data
        db: Database session
        payload: Validated token payload
        
    Returns:
        ServiceReviewResponse: Created service review
    """
    return await car_service.create_review(review, db, payload)

@router.put("/review/{service_id}", response_model=ServiceReviewResponse)
async def update_review_by_id(service_id: int, review: ServiceReviewUpdate, db: Session = Depends(get_postgres_db), payload = Security(validate_token, scopes=["UPDATE:SERVICE_REVIEWS"])):
    """
    Update a service review.
    
    Args:
        service_id: Service ID
        review: Updated review data
        db: Database session
        payload: Validated token payload
        
    Returns:
        ServiceReviewResponse: Updated service review
    """
    return await car_service.update_review_by_id(service_id, review, db, payload)

@router.delete("/review/{service_id}", response_class=JSONResponse)
async def delete_review_by_id(service_id: int, db: Session = Depends(get_postgres_db), payload = Security(validate_token, scopes=["DELETE:SERVICE_REVIEWS"])):
    """
    Delete a service review.
    
    Args:
        service_id: Service ID
        db: Database session
        payload: Validated token payload
        
    Returns:
        JSONResponse: Success message
    """
    return await car_service.delete_review_by_id(service_id, db, payload)


# service routes
@router.get("/", response_model=List[ServiceResponse])
async def get_services_by_category_id(category_id: Optional[int] = None, db: Session = Depends(get_postgres_db), payload = Security(validate_token, scopes=["READ:SERVICES", "READ:PRICE_CHART"])):
    """
    Get all services, optionally filtered by category.
    
    Args:
        category_id: Optional category ID to filter by
        db: Database session
        payload: Validated token payload
        
    Returns:
        List[ServiceResponse]: List of services
    """
    filters = {"category_id": category_id} if category_id else None
    return await crud.get_all_records(db, Service, filters=filters)

@router.get("/{service_id}", response_model=ServiceResponse)
async def get_services_by_service_id(service_id: int, db: Session = Depends(get_postgres_db), payload = Security(validate_token, scopes=["READ:SERVICES", "READ:PRICE_CHART"])):
    """
    Get a service by ID.
    
    Args:
        service_id: Service ID
        db: Database session
        payload: Validated token payload
        
    Returns:
        ServiceResponse: Service information
    """
    return await crud.get_record_by_primary_key(db, service_id, Service)

@router.post("/", response_model=ServiceResponse)
async def create_service(service: ServiceCreate, db: Session = Depends(get_postgres_db), payload = Security(validate_token, scopes=["WRITE:SERVICES", "WRITE:PRICE_CHART"])):
    """
    Create a new service.
    
    Args:
        service: Service creation data
        db: Database session
        payload: Validated token payload
        
    Returns:
        ServiceResponse: Created service
    """
    return await car_service.create_service(db, service.model_dump())

@router.put("/{id}", response_model=ServiceResponse)
async def update_service_by_id(id: int, service: ServiceUpdateWithForeignData, db: Session = Depends(get_postgres_db), payload = Security(validate_token, scopes=["UPDATE:SERVICES", "UPDATE:PRICE_CHART"])):
    """
    Update a service.
    
    Args:
        id: Service ID
        service: Updated service data
        db: Database session
        payload: Validated token payload
        
    Returns:
        ServiceResponse: Updated service
    """
    return await car_service.update_service(db, id, service)

@router.delete("/{id}", response_class=JSONResponse)
async def delete_service_by_id(id: int, db: Session = Depends(get_postgres_db), payload = Security(validate_token, scopes=["DELETE:SERVICES", "DELETE:PRICE_CHART"])):
    """
    Delete a service.
    
    Args:
        id: Service ID
        db: Database session
        payload: Validated token payload
        
    Returns:
        JSONResponse: Success message
    """
    message = await crud.delete_record_by_primary_key(db, id, Service)
    return JSONResponse(content=message)