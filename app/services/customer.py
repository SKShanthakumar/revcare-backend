from fastapi import HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession as Session
from app.services import crud
from app.models import Cart, Favourite

async def add_to_cart(service_id: int, db: Session, payload: dict):
    customer_id = payload.get("user_id")
    if not customer_id.startswith("CST"):
        raise HTTPException(status_code=403, detail="Operation not permitted. Only Customers can add services to cart")
    
    data = {
        "service_id": service_id,
        "customer_id": customer_id
    }
    try:
        await crud.create_record(db, data, Cart)
        return JSONResponse(content={"message": "Service added to cart successfully."})
    except HTTPException as e:
        if "foreign key" in e.detail:
            raise HTTPException(
                status_code=400,
                detail="Service already added to cart."
            )
        raise

async def remove_from_cart(service_id: int, db: Session, payload: dict):
    customer_id = payload.get("user_id")
    if not customer_id.startswith("CST"):
        raise HTTPException(status_code=403, detail="Operation not permitted. Only Customers can remove services from cart")
    
    # build composite primary key
    pk = {
        "customer_id": customer_id,
        "service_id": service_id
    }
    try:
        await crud.delete_record_by_composite_key(db, pk, Cart)
        return JSONResponse(content={"message": "Service removed from cart successfully."})
    except HTTPException as e:
        if "not found" in e.detail:
            raise HTTPException(
                status_code=400,
                detail="Service not in cart."
            )
        raise


async def add_to_favourite(service_id: int, db: Session, payload: dict):
    customer_id = payload.get("user_id")
    if not customer_id.startswith("CST"):
        raise HTTPException(status_code=403, detail="Operation not permitted. Only Customers can add services to favourite")
    
    data = {
        "service_id": service_id,
        "customer_id": customer_id
    }
    try:
        await crud.create_record(db, data, Favourite)
        return JSONResponse(content={"message": "Service added to favourite successfully."})
    except HTTPException as e:
        if "foreign key" in e.detail:
            raise HTTPException(
                status_code=400,
                detail="Service already added to favourite."
            )
        raise

async def remove_from_favourite(service_id: int, db: Session, payload: dict):
    customer_id = payload.get("user_id")
    if not customer_id.startswith("CST"):
        raise HTTPException(status_code=403, detail="Operation not permitted. Only Customers can remove services from favourite")
    
    # build composite primary key
    pk = {
        "customer_id": customer_id,
        "service_id": service_id
    }
    try:
        await crud.delete_record_by_composite_key(db, pk, Favourite)
        return JSONResponse(content={"message": "Service removed from favourite successfully."})
    except HTTPException as e:
        if "not found" in e.detail:
            raise HTTPException(
                status_code=400,
                detail="Service not in favourite."
            )
        raise
