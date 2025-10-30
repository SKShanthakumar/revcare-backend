from fastapi import APIRouter, Depends, Security, HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession as Session
from typing import List
from app.database.dependencies import get_postgres_db
from app.models import Customer
from app.schemas import CustomerCreate, CustomerResponse, CustomerUpdate
from app.services import user
from app.auth.dependencies import validate_token

router = APIRouter()

@router.get("/", response_model=List[CustomerResponse])
async def get_all_customers(db: Session = Depends(get_postgres_db), payload = Security(validate_token, scopes=["READ:CUSTOMERS"])):
    return await user.get_all_users(db, Customer)

@router.post("/", response_model=CustomerResponse)
async def create_customer(customer: CustomerCreate, db: Session = Depends(get_postgres_db)):
    return await user.create_user(db, customer, Customer)
    
@router.get("/{id}", response_model=CustomerResponse)
async def get_customer_by_id(id: str, db: Session = Depends(get_postgres_db), payload = Security(validate_token, scopes=["READ:CUSTOMERS"])):
    return await user.get_user_by_id(db, id.strip(), Customer)

@router.put("/{id}", response_model=CustomerResponse)
async def update_customer(id: str, customer_data: CustomerUpdate, db: Session = Depends(get_postgres_db), payload = Security(validate_token, scopes=["UPDATE:CUSTOMERS"])):
    if payload.get("role") != 1 and payload.get("user_id") != id:
        raise HTTPException(status_code=403, detail="Operation not permitted.")
    
    return await user.update_user(db, id.strip(), customer_data, Customer)

@router.delete("/{id}", response_class=JSONResponse)
async def delete_customer(id: str, db: Session = Depends(get_postgres_db), payload = Security(validate_token, scopes=["DELETE:CUSTOMERS"])):
    if payload.get("role") != 1 and payload.get("user_id") != id:
        raise HTTPException(status_code=403, detail="Operation not permitted.")
    
    message = await user.delete_user(db, id.strip(), Customer)
    return JSONResponse(content=message)