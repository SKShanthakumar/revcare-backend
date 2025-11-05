from fastapi import APIRouter, Depends, Security
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession as Session
from typing import List, Optional
from app.database.dependencies import get_postgres_db
from app.models import Car, CarClass, CustomerCar, Manufacturer, FuelType
from app.schemas import CustomerCarResponse, CustomerCarCreate, CustomerCarUpdate, CarCreate, CarResponse, CarUpdate, CarClassResponse, CarClassCreate, CarClassUpdate, FuelTypeCreate, FuelTypeResponse, FuelTypeUpdate, ManufacturerCreate, ManufacturerResponse, ManufacturerUpdate
from app.services import crud, car as car_service
from app.auth.dependencies import validate_token

router = APIRouter()

# car model routes
@router.get("/models", response_model=List[CarResponse])
async def get_car_models(db: Session = Depends(get_postgres_db), payload = Security(validate_token, scopes=["READ:CARS"])):
    return await crud.get_all_records(db, Car)

@router.post("/models", response_model=CarResponse)
async def create_car_model(car_model: CarCreate, db: Session = Depends(get_postgres_db), payload = Security(validate_token, scopes=["WRITE:CARS"])):
    return await crud.create_record(db, car_model.model_dump(), Car)

@router.put("/models/{id}", response_model=CarResponse)
async def update_car_model_by_id(id: int, car_model: CarUpdate, db: Session = Depends(get_postgres_db), payload = Security(validate_token, scopes=["UPDATE:CARS"])):
    return await crud.update_record_by_primary_key(db, id, car_model.model_dump(exclude_none=True), Car)

@router.delete("/models/{id}", response_class=JSONResponse)
async def delete_car_model_by_id(id: int, db: Session = Depends(get_postgres_db), payload = Security(validate_token, scopes=["DELETE:CARS"])):
    message = await crud.delete_record_by_primary_key(db, id, Car)
    return JSONResponse(content=message)


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


# customer car routes
@router.get("/", response_model=List[CustomerCarResponse])
async def get_customer_cars(customer_id: Optional[str] = None, db: Session = Depends(get_postgres_db), payload = Security(validate_token, scopes=["READ:CUSTOMER_CARS"])):
    return await car_service.get_customer_cars(db, payload, customer_id)

@router.get("/{id}", response_model=CustomerCarResponse)
async def get_customer_car_by_id(id: int, db: Session = Depends(get_postgres_db), payload = Security(validate_token, scopes=["READ:CUSTOMER_CARS"])):
    return await crud.get_record_by_primary_key(db, id, CustomerCar)

@router.post("/", response_model=CustomerCarResponse)
async def create_customer_car(customer_car: CustomerCarCreate, db: Session = Depends(get_postgres_db), payload = Security(validate_token, scopes=["WRITE:CUSTOMER_CARS"])):
    return await car_service.create_customer_car(customer_car, db, payload)

@router.put("/{id}", response_model=CustomerCarResponse)
async def update_customer_car_by_id(id: int, customer_car: CustomerCarUpdate, db: Session = Depends(get_postgres_db), payload = Security(validate_token, scopes=["UPDATE:CUSTOMER_CARS"])):
    return await car_service.update_customer_car_by_id(id, customer_car, db, payload)

@router.delete("/{id}", response_class=JSONResponse)
async def delete_customer_car_by_id(id: int, db: Session = Depends(get_postgres_db), payload = Security(validate_token, scopes=["DELETE:CUSTOMER_CARS"])):
    return await car_service.delete_customer_car_by_id(id, db, payload)
