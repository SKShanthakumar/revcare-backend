from fastapi import APIRouter, Depends, Security, HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession as Session
from typing import List, Optional
from app.database.dependencies import get_postgres_db
from app.models import ServiceCategory, Service
from app.schemas import ServiceCategoryCreate, ServiceCategoryResponse, ServiceCategoryUpdate, ServiceCreate, ServiceResponse, ServiceUpdate
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


# service routes
@router.get("/", response_model=List[ServiceResponse])
async def get_services_by_category_id(category_id: Optional[int] = None, db: Session = Depends(get_postgres_db), payload = Security(validate_token, scopes=["READ:SERVICES"])):
    filters = {"category_id": category_id} if category_id else None
    return await crud.get_all_records(db, Service, filters=filters)

@router.post("/", response_model=ServiceResponse)
async def create_service(service: ServiceCreate, db: Session = Depends(get_postgres_db), payload = Security(validate_token, scopes=["WRITE:SERVICES"])):
    return await car_service.create_service(db, service.model_dump())

@router.put("/{id}", response_model=ServiceResponse)
async def update_service_by_id(id: int, service: ServiceUpdate, db: Session = Depends(get_postgres_db), payload = Security(validate_token, scopes=["UPDATE:SERVICES"])):
    pass

@router.delete("/{id}", response_class=JSONResponse)
async def delete_service_by_id(id: int, db: Session = Depends(get_postgres_db), payload = Security(validate_token, scopes=["DELETE:SERVICES"])):
    pass