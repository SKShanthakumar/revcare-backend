from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from typing import List
from app.database.dependencies import get_postgres_db
from app.models import Customer
from app.schemas import CustomerCreate, CustomerResponse, CustomerUpdate
from app.controllers import user

router = APIRouter()

@router.get("/", response_model=List[CustomerResponse])
def get_all_customers(db: Session = Depends(get_postgres_db)):
    return user.get_all_users(db, Customer)

@router.post("/", response_model=CustomerResponse)
def create_customer(customer: CustomerCreate, db: Session = Depends(get_postgres_db)):
    return user.create_user(db, customer, Customer)
    
@router.get("/{id}", response_model=CustomerResponse)
def get_customer_by_id(id: str, db: Session = Depends(get_postgres_db)):
    return user.get_user_by_id(db, id.strip(), Customer)

@router.put("/{id}", response_model=CustomerResponse)
def update_customer(id: str, customer_data: CustomerUpdate, db: Session = Depends(get_postgres_db)):
    return user.update_user(db, id.strip(), customer_data, Customer)

@router.delete("/{id}", response_class=JSONResponse)
def delete_customer(id: str, db: Session = Depends(get_postgres_db)):
    message = user.delete_user(db, id.strip(), Customer)
    return JSONResponse(content=message)