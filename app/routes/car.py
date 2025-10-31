from fastapi import APIRouter, Depends, Security, HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession as Session
from typing import List
from app.database.dependencies import get_postgres_db
from app.models import Car, CarClass, CustomerCar, Manufacturer, FuelType
from app.schemas import CarClassResponse, CarClassCreate, CarClassUpdate, FuelTypeCreate, FuelTypeResponse, FuelTypeUpdate, ManufacturerCreate, ManufacturerResponse, ManufacturerUpdate
from app.services import crud
from app.auth.dependencies import validate_token

router = APIRouter()

# car class routes
@router.get("/class", response_model=List[CarClassResponse])
async def get_car_classes(db: Session = Depends(get_postgres_db), payload = Security(validate_token, scopes=["READ:UTILS"])):
    return await crud.get_all_records(db, CarClass)

@router.post("/class", response_model=CarClassResponse)
async def create_car_class(car_class: CarClassCreate, db: Session = Depends(get_postgres_db), payload = Security(validate_token, scopes=["WRITE:UTILS"])):
    return await crud.create_record(db, car_class.model_dump(), CarClass)

@router.put("/class/{id}", response_model=CarClassResponse)
async def update_car_class_by_id(id: int, car_class: CarClassUpdate, db: Session = Depends(get_postgres_db), payload = Security(validate_token, scopes=["UPDATE:UTILS"])):
    return await crud.update_record_by_primary_key(db, id, car_class.model_dump(exclude_none=True), CarClass)

@router.delete("/class/{id}", response_class=JSONResponse)
async def delete_car_class_by_id(id: int, db: Session = Depends(get_postgres_db), payload = Security(validate_token, scopes=["DELETE:UTILS"])):
    message = await crud.delete_record_by_primary_key(db, id, CarClass)
    return JSONResponse(content=message)

# Fuel type routes
@router.get("/fuel", response_model=List[FuelTypeResponse])
async def get_fuel_types(db: Session = Depends(get_postgres_db), payload = Security(validate_token, scopes=["READ:UTILS"])):
    return await crud.get_all_records(db, FuelType)

@router.post("/fuel", response_model=FuelTypeResponse)
async def create_fuel_type(fuel: FuelTypeCreate, db: Session = Depends(get_postgres_db), payload = Security(validate_token, scopes=["WRITE:UTILS"])):
    return await crud.create_record(db, fuel.model_dump(), FuelType)

@router.put("/fuel/{id}", response_model=FuelTypeResponse)
async def update_fuel_type_by_id(id: int, fuel: FuelTypeUpdate, db: Session = Depends(get_postgres_db), payload = Security(validate_token, scopes=["UPDATE:UTILS"])):
    return await crud.update_record_by_primary_key(db, id, fuel.model_dump(exclude_none=True), FuelType)

@router.delete("/fuel/{id}", response_class=JSONResponse)
async def delete_fuel_type_by_id(id: int, db: Session = Depends(get_postgres_db), payload = Security(validate_token, scopes=["DELETE:UTILS"])):
    message = await crud.delete_record_by_primary_key(db, id, FuelType)
    return JSONResponse(content=message)

# manufacturers routes
@router.get("/manufacturer", response_model=List[ManufacturerResponse])
async def get_manufacturers(db: Session = Depends(get_postgres_db), payload = Security(validate_token, scopes=["READ:UTILS"])):
    return await crud.get_all_records(db, Manufacturer)

@router.post("/manufacturer", response_model=ManufacturerResponse)
async def create_manufacturer(manufacturer: ManufacturerCreate, db: Session = Depends(get_postgres_db), payload = Security(validate_token, scopes=["WRITE:UTILS"])):
    return await crud.create_record(db, manufacturer.model_dump(), Manufacturer)

@router.put("/manufacturer/{id}", response_model=ManufacturerResponse)
async def update_manufacturer_by_id(id: int, manufacturer: ManufacturerUpdate, db: Session = Depends(get_postgres_db), payload = Security(validate_token, scopes=["UPDATE:UTILS"])):
    return await crud.update_record_by_primary_key(db, id, manufacturer.model_dump(exclude_none=True), Manufacturer)

@router.delete("/manufacturer/{id}", response_class=JSONResponse)
async def delete_manufacturer_by_id(id: int, db: Session = Depends(get_postgres_db), payload = Security(validate_token, scopes=["DELETE:UTILS"])):
    message = await crud.delete_record_by_primary_key(db, id, Manufacturer)
    return JSONResponse(content=message)

