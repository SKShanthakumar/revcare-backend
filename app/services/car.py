from fastapi import HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession as Session
from app.models import CustomerCar
from app.services import crud
from app.schemas import CustomerCarUpdate, CustomerCarCreate

async def get_customer_cars(db: Session, payload: dict, customer_id: str):
    filters = None
    if customer_id is not None:
        if payload.get("role") == 3 and (customer_id != payload.get("user_id")):
            raise HTTPException(status_code=403, detail="Operation not permitted. Trying to access data of other customers.")
        
        filters = {"customer_id": customer_id}
    else:
        user_id = payload.get("user_id")
        if user_id.startswith("CST"):
            filters = {"customer_id": user_id}

    return await crud.get_all_records(db, CustomerCar, filters=filters)


async def get_customer_car_by_id(customer_car_id: int, db: Session, payload: dict):
    customer_car = await crud.get_record_by_primary_key(db, customer_car_id, CustomerCar)

    customer_id = payload.get("user_id")
    if payload.get("role") == 3 and (customer_id != customer_car.customer_id):
        raise HTTPException(status_code=403, detail="Operation not permitted. Trying to access data of other customers.")
        
    return customer_car

async def create_customer_car(customer_car: CustomerCarCreate, db: Session, payload: dict):
    customer_id = payload.get("user_id")
    
    if not customer_id.startswith("CST"):
        raise HTTPException(status_code=403, detail="Operation not permitted.")
    
    customer_car_dict = customer_car.model_dump()
    customer_car_dict["customer_id"] = customer_id

    return await crud.create_record(db, customer_car_dict, CustomerCar)


async def update_customer_car_by_id(id: int, customer_car: CustomerCarUpdate, db: Session, payload: dict):
    customer_car_obj = await get_customer_car_by_id(id, db, payload)
    if not customer_car:
        raise HTTPException(status_code=404, detail=f"Car not found.")
    
    for key, value in customer_car.model_dump(exclude_none=True).items():
        if hasattr(customer_car_obj, key):
            setattr(customer_car_obj, key, value)
    
    await db.commit()
    await db.refresh(customer_car_obj)
    return customer_car_obj


async def delete_customer_car_by_id(id: int, db: Session, payload: dict):
    customer_car = await get_customer_car_by_id(id, db, payload)
    if not customer_car:
        raise HTTPException(status_code=404, detail="Car not found.")

    await db.delete(customer_car)
    await db.commit()

    message = {"detail": "Car deleted successfully."}
    return JSONResponse(content=message)
