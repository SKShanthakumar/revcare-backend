from fastapi import APIRouter, Depends, Security, HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession as Session
from typing import List, Optional
from app.database.dependencies import get_postgres_db
from app.models import Customer, Cart, Favourite
from app.schemas import CustomerCreate, CustomerResponse, CustomerUpdate
from app.services import crud, user, customer as customer_service
from app.auth.dependencies import validate_token

router = APIRouter()

# cart routes
@router.post("/cart/{service_id}", response_class=JSONResponse)
async def add_to_cart(service_id: int, db: Session = Depends(get_postgres_db), payload = Security(validate_token, scopes=["WRITE:CART"])):
    return await customer_service.add_to_cart(service_id, db, payload)

@router.delete("/cart/{service_id}", response_class=JSONResponse)
async def remove_from_cart(service_id: int, db: Session = Depends(get_postgres_db), payload = Security(validate_token, scopes=["DELETE:CART"])):
    return await customer_service.remove_from_cart(service_id, db, payload)


# favourite services routes
@router.post("/favourite/{service_id}", response_class=JSONResponse)
async def add_to_favourite(service_id: int, db: Session = Depends(get_postgres_db), payload = Security(validate_token, scopes=["WRITE:FAVOURITES"])):
    return await customer_service.add_to_favourite(service_id, db, payload)

@router.delete("/favourite/{service_id}", response_class=JSONResponse)
async def remove_from_favourite(service_id: int, db: Session = Depends(get_postgres_db), payload = Security(validate_token, scopes=["DELETE:FAVOURITES"])):
    return await customer_service.remove_from_favourite(service_id, db, payload)


# customer data based routes
@router.get("/", response_model=List[CustomerResponse])
async def get_customers(customer_id: Optional[str] = None, db: Session = Depends(get_postgres_db), payload = Security(validate_token, scopes=["READ:CUSTOMERS"])):
    return await user.get_customers(db, payload, customer_id)

@router.post("/", response_model=CustomerResponse)
async def create_customer(customer: CustomerCreate, db: Session = Depends(get_postgres_db)):
    return await user.create_user(db, customer, Customer)
    
@router.put("/{id}", response_model=CustomerResponse)
async def update_customer(id: str, customer_data: CustomerUpdate, db: Session = Depends(get_postgres_db), payload = Security(validate_token, scopes=["UPDATE:CUSTOMERS"])):
    return await user.update_customer(id, customer_data, db, payload)

@router.delete("/{id}", response_class=JSONResponse)
async def delete_customer(id: str, db: Session = Depends(get_postgres_db), payload = Security(validate_token, scopes=["DELETE:CUSTOMERS"])):
    return await user.delete_customer(id, db, payload)