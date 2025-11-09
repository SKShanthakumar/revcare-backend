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
    """
    Get all car models.
    
    Args:
        db: Database session
        payload: Validated token payload
        
    Returns:
        List[CarResponse]: List of car models
    """
    return await crud.get_all_records(db, Car)

@router.post("/models", response_model=CarResponse)
async def create_car_model(car_model: CarCreate, db: Session = Depends(get_postgres_db), payload = Security(validate_token, scopes=["WRITE:CARS"])):
    """
    Create a new car model.
    
    Args:
        car_model: Car model creation data
        db: Database session
        payload: Validated token payload
        
    Returns:
        CarResponse: Created car model
    """
    return await crud.create_record(db, car_model.model_dump(), Car)

@router.put("/models/{id}", response_model=CarResponse)
async def update_car_model_by_id(id: int, car_model: CarUpdate, db: Session = Depends(get_postgres_db), payload = Security(validate_token, scopes=["UPDATE:CARS"])):
    """
    Update a car model.
    
    Args:
        id: Car model ID
        car_model: Updated car model data
        db: Database session
        payload: Validated token payload
        
    Returns:
        CarResponse: Updated car model
    """
    return await crud.update_record_by_primary_key(db, id, car_model.model_dump(exclude_none=True), Car)

@router.delete("/models/{id}", response_class=JSONResponse)
async def delete_car_model_by_id(id: int, db: Session = Depends(get_postgres_db), payload = Security(validate_token, scopes=["DELETE:CARS"])):
    """
    Delete a car model.
    
    Args:
        id: Car model ID
        db: Database session
        payload: Validated token payload
        
    Returns:
        JSONResponse: Success message
    """
    message = await crud.delete_record_by_primary_key(db, id, Car)
    return JSONResponse(content=message)


# car class routes
@router.get("/class", response_model=List[CarClassResponse])
async def get_car_classes(db: Session = Depends(get_postgres_db), payload = Security(validate_token, scopes=["READ:UTILS"])):
    """
    Get all car classes.
    
    Args:
        db: Database session
        payload: Validated token payload
        
    Returns:
        List[CarClassResponse]: List of car classes
    """
    return await crud.get_all_records(db, CarClass)

@router.post("/class", response_model=CarClassResponse)
async def create_car_class(car_class: CarClassCreate, db: Session = Depends(get_postgres_db), payload = Security(validate_token, scopes=["WRITE:UTILS"])):
    """
    Create a new car class.
    
    Args:
        car_class: Car class creation data
        db: Database session
        payload: Validated token payload
        
    Returns:
        CarClassResponse: Created car class
    """
    return await crud.create_record(db, car_class.model_dump(), CarClass)

@router.put("/class/{id}", response_model=CarClassResponse)
async def update_car_class_by_id(id: int, car_class: CarClassUpdate, db: Session = Depends(get_postgres_db), payload = Security(validate_token, scopes=["UPDATE:UTILS"])):
    """
    Update a car class.
    
    Args:
        id: Car class ID
        car_class: Updated car class data
        db: Database session
        payload: Validated token payload
        
    Returns:
        CarClassResponse: Updated car class
    """
    return await crud.update_record_by_primary_key(db, id, car_class.model_dump(exclude_none=True), CarClass)

@router.delete("/class/{id}", response_class=JSONResponse)
async def delete_car_class_by_id(id: int, db: Session = Depends(get_postgres_db), payload = Security(validate_token, scopes=["DELETE:UTILS"])):
    """
    Delete a car class.
    
    Args:
        id: Car class ID
        db: Database session
        payload: Validated token payload
        
    Returns:
        JSONResponse: Success message
    """
    message = await crud.delete_record_by_primary_key(db, id, CarClass)
    return JSONResponse(content=message)


# Fuel type routes
@router.get("/fuel", response_model=List[FuelTypeResponse])
async def get_fuel_types(db: Session = Depends(get_postgres_db), payload = Security(validate_token, scopes=["READ:UTILS"])):
    """
    Get all fuel types.
    
    Args:
        db: Database session
        payload: Validated token payload
        
    Returns:
        List[FuelTypeResponse]: List of fuel types
    """
    return await crud.get_all_records(db, FuelType)

@router.post("/fuel", response_model=FuelTypeResponse)
async def create_fuel_type(fuel: FuelTypeCreate, db: Session = Depends(get_postgres_db), payload = Security(validate_token, scopes=["WRITE:UTILS"])):
    """
    Create a new fuel type.
    
    Args:
        fuel: Fuel type creation data
        db: Database session
        payload: Validated token payload
        
    Returns:
        FuelTypeResponse: Created fuel type
    """
    return await crud.create_record(db, fuel.model_dump(), FuelType)

@router.put("/fuel/{id}", response_model=FuelTypeResponse)
async def update_fuel_type_by_id(id: int, fuel: FuelTypeUpdate, db: Session = Depends(get_postgres_db), payload = Security(validate_token, scopes=["UPDATE:UTILS"])):
    """
    Update a fuel type.
    
    Args:
        id: Fuel type ID
        fuel: Updated fuel type data
        db: Database session
        payload: Validated token payload
        
    Returns:
        FuelTypeResponse: Updated fuel type
    """
    return await crud.update_record_by_primary_key(db, id, fuel.model_dump(exclude_none=True), FuelType)

@router.delete("/fuel/{id}", response_class=JSONResponse)
async def delete_fuel_type_by_id(id: int, db: Session = Depends(get_postgres_db), payload = Security(validate_token, scopes=["DELETE:UTILS"])):
    """
    Delete a fuel type.
    
    Args:
        id: Fuel type ID
        db: Database session
        payload: Validated token payload
        
    Returns:
        JSONResponse: Success message
    """
    message = await crud.delete_record_by_primary_key(db, id, FuelType)
    return JSONResponse(content=message)


# manufacturers routes
@router.get("/manufacturer", response_model=List[ManufacturerResponse])
async def get_manufacturers(db: Session = Depends(get_postgres_db), payload = Security(validate_token, scopes=["READ:UTILS"])):
    """
    Get all manufacturers.
    
    Args:
        db: Database session
        payload: Validated token payload
        
    Returns:
        List[ManufacturerResponse]: List of manufacturers
    """
    return await crud.get_all_records(db, Manufacturer)

@router.post("/manufacturer", response_model=ManufacturerResponse)
async def create_manufacturer(manufacturer: ManufacturerCreate, db: Session = Depends(get_postgres_db), payload = Security(validate_token, scopes=["WRITE:UTILS"])):
    """
    Create a new manufacturer.
    
    Args:
        manufacturer: Manufacturer creation data
        db: Database session
        payload: Validated token payload
        
    Returns:
        ManufacturerResponse: Created manufacturer
    """
    return await crud.create_record(db, manufacturer.model_dump(), Manufacturer)

@router.put("/manufacturer/{id}", response_model=ManufacturerResponse)
async def update_manufacturer_by_id(id: int, manufacturer: ManufacturerUpdate, db: Session = Depends(get_postgres_db), payload = Security(validate_token, scopes=["UPDATE:UTILS"])):
    """
    Update a manufacturer.
    
    Args:
        id: Manufacturer ID
        manufacturer: Updated manufacturer data
        db: Database session
        payload: Validated token payload
        
    Returns:
        ManufacturerResponse: Updated manufacturer
    """
    return await crud.update_record_by_primary_key(db, id, manufacturer.model_dump(exclude_none=True), Manufacturer)

@router.delete("/manufacturer/{id}", response_class=JSONResponse)
async def delete_manufacturer_by_id(id: int, db: Session = Depends(get_postgres_db), payload = Security(validate_token, scopes=["DELETE:UTILS"])):
    """
    Delete a manufacturer.
    
    Args:
        id: Manufacturer ID
        db: Database session
        payload: Validated token payload
        
    Returns:
        JSONResponse: Success message
    """
    message = await crud.delete_record_by_primary_key(db, id, Manufacturer)
    return JSONResponse(content=message)


# customer car routes
@router.get("/", response_model=List[CustomerCarResponse])
async def get_customer_cars(customer_id: Optional[str] = None, db: Session = Depends(get_postgres_db), payload = Security(validate_token, scopes=["READ:CUSTOMER_CARS"])):
    """
    Get customer cars.
    
    Args:
        customer_id: Optional customer ID to filter by
        db: Database session
        payload: Validated token payload
        
    Returns:
        List[CustomerCarResponse]: List of customer cars
    """
    return await car_service.get_customer_cars(db, payload, customer_id)

@router.get("/{id}", response_model=CustomerCarResponse)
async def get_customer_car_by_id(id: int, db: Session = Depends(get_postgres_db), payload = Security(validate_token, scopes=["READ:CUSTOMER_CARS"])):
    """
    Get a customer car by ID.
    
    Args:
        id: Customer car ID
        db: Database session
        payload: Validated token payload
        
    Returns:
        CustomerCarResponse: Customer car information
    """
    return await crud.get_record_by_primary_key(db, id, CustomerCar)

@router.post("/", response_model=CustomerCarResponse)
async def create_customer_car(customer_car: CustomerCarCreate, db: Session = Depends(get_postgres_db), payload = Security(validate_token, scopes=["WRITE:CUSTOMER_CARS"])):
    """
    Create a new customer car.
    
    Args:
        customer_car: Customer car creation data
        db: Database session
        payload: Validated token payload
        
    Returns:
        CustomerCarResponse: Created customer car
    """
    return await car_service.create_customer_car(customer_car, db, payload)

@router.put("/{id}", response_model=CustomerCarResponse)
async def update_customer_car_by_id(id: int, customer_car: CustomerCarUpdate, db: Session = Depends(get_postgres_db), payload = Security(validate_token, scopes=["UPDATE:CUSTOMER_CARS"])):
    """
    Update a customer car.
    
    Args:
        id: Customer car ID
        customer_car: Updated customer car data
        db: Database session
        payload: Validated token payload
        
    Returns:
        CustomerCarResponse: Updated customer car
    """
    return await car_service.update_customer_car_by_id(id, customer_car, db, payload)

@router.delete("/{id}", response_class=JSONResponse)
async def delete_customer_car_by_id(id: int, db: Session = Depends(get_postgres_db), payload = Security(validate_token, scopes=["DELETE:CUSTOMER_CARS"])):
    """
    Delete a customer car.
    
    Args:
        id: Customer car ID
        db: Database session
        payload: Validated token payload
        
    Returns:
        JSONResponse: Success message
    """
    return await car_service.delete_customer_car_by_id(id, db, payload)
