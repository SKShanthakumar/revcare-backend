from fastapi import APIRouter, Depends, Security, HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession as Session
from typing import List
from app.database.dependencies import get_postgres_db
from app.models import Customer, Cart, Favourite
from app.schemas import CustomerCreate, CustomerResponse, CustomerUpdate
from app.services import crud, user
from app.auth.dependencies import validate_token

router = APIRouter()

# cart routes
@router.post("/cart/{service_id}", response_class=JSONResponse)
async def add_to_cart(service_id: int, db: Session = Depends(get_postgres_db), payload = Security(validate_token, scopes=["WRITE:CART"])):
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

@router.delete("/cart/{service_id}", response_class=JSONResponse)
async def remove_from_cart(service_id: int, db: Session = Depends(get_postgres_db), payload = Security(validate_token, scopes=["DELETE:CART"])):
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


# favourite services routes
@router.post("/favourite/{service_id}", response_class=JSONResponse)
async def add_to_favourite(service_id: int, db: Session = Depends(get_postgres_db), payload = Security(validate_token, scopes=["WRITE:FAVOURITES"])):
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

@router.delete("/favourite/{service_id}", response_class=JSONResponse)
async def remove_from_favourite(service_id: int, db: Session = Depends(get_postgres_db), payload = Security(validate_token, scopes=["DELETE:FAVOURITES"])):
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

# customer data based routes
@router.get("/", response_model=List[CustomerResponse])
async def get_all_customers(db: Session = Depends(get_postgres_db), payload = Security(validate_token, scopes=["READ:CUSTOMERS"])):
    return await crud.get_all_records(db, Customer)

@router.post("/", response_model=CustomerResponse)
async def create_customer(customer: CustomerCreate, db: Session = Depends(get_postgres_db)):
    return await user.create_user(db, customer, Customer)
    
@router.get("/{id}", response_model=CustomerResponse)
async def get_customer_by_id(id: str, db: Session = Depends(get_postgres_db), payload = Security(validate_token, scopes=["READ:CUSTOMERS"])):
    return await crud.get_record_by_primary_key(db, id.strip(), Customer)

@router.put("/{id}", response_model=CustomerResponse)
async def update_customer(id: str, customer_data: CustomerUpdate, db: Session = Depends(get_postgres_db), payload = Security(validate_token, scopes=["UPDATE:CUSTOMERS"])):
    if payload.get("role") == 3 and payload.get("user_id") != id:
        raise HTTPException(status_code=403, detail="Operation not permitted. Trying to access data of other customers.")
    
    return await crud.update_record_by_primary_key(db, id.strip(), customer_data.model_dump(exclude_none=True), Customer)

@router.delete("/{id}", response_class=JSONResponse)
async def delete_customer(id: str, db: Session = Depends(get_postgres_db), payload = Security(validate_token, scopes=["DELETE:CUSTOMERS"])):
    if payload.get("role") == 3 and payload.get("user_id") != id:
        raise HTTPException(status_code=403, detail="Operation not permitted. Trying to access data of other customers.")
    
    message = await crud.delete_record_by_primary_key(db, id.strip(), Customer)
    return JSONResponse(content=message)

