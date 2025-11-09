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
    """
    Add a service to the customer's cart.
    
    Args:
        service_id: ID of the service to add to cart
        db: Database session
        payload: Validated token payload
        
    Returns:
        JSONResponse: Success message
    """
    return await customer_service.add_to_cart(service_id, db, payload)

@router.delete("/cart/{service_id}", response_class=JSONResponse)
async def remove_from_cart(service_id: int, db: Session = Depends(get_postgres_db), payload = Security(validate_token, scopes=["DELETE:CART"])):
    """
    Remove a service from the customer's cart.
    
    Args:
        service_id: ID of the service to remove from cart
        db: Database session
        payload: Validated token payload
        
    Returns:
        JSONResponse: Success message
    """
    return await customer_service.remove_from_cart(service_id, db, payload)


# favourite services routes
@router.post("/favourite/{service_id}", response_class=JSONResponse)
async def add_to_favourite(service_id: int, db: Session = Depends(get_postgres_db), payload = Security(validate_token, scopes=["WRITE:FAVOURITES"])):
    """
    Add a service to the customer's favourites.
    
    Args:
        service_id: ID of the service to add to favourites
        db: Database session
        payload: Validated token payload
        
    Returns:
        JSONResponse: Success message
    """
    return await customer_service.add_to_favourite(service_id, db, payload)

@router.delete("/favourite/{service_id}", response_class=JSONResponse)
async def remove_from_favourite(service_id: int, db: Session = Depends(get_postgres_db), payload = Security(validate_token, scopes=["DELETE:FAVOURITES"])):
    """
    Remove a service from the customer's favourites.
    
    Args:
        service_id: ID of the service to remove from favourites
        db: Database session
        payload: Validated token payload
        
    Returns:
        JSONResponse: Success message
    """
    return await customer_service.remove_from_favourite(service_id, db, payload)


# customer data based routes
@router.get("/", response_model=List[CustomerResponse])
async def get_customers(customer_id: Optional[str] = None, db: Session = Depends(get_postgres_db), payload = Security(validate_token, scopes=["READ:CUSTOMERS"])):
    """
    Get customer(s) information.
    
    If customer_id is provided, returns that specific customer.
    Otherwise, returns all customers based on user permissions.
    
    Args:
        customer_id: Optional customer ID to filter by
        db: Database session
        payload: Validated token payload
        
    Returns:
        List[CustomerResponse]: List of customer information
    """
    return await user.get_customers(db, payload, customer_id)

@router.post("/", response_model=CustomerResponse)
async def create_customer(customer: CustomerCreate, db: Session = Depends(get_postgres_db)):
    """
    Create a new customer account.
    
    Args:
        customer: Customer creation data
        db: Database session
        
    Returns:
        CustomerResponse: Created customer information
    """
    return await user.create_user(db, customer, Customer)
    
@router.put("/{id}", response_model=CustomerResponse)
async def update_customer(id: str, customer_data: CustomerUpdate, db: Session = Depends(get_postgres_db), payload = Security(validate_token, scopes=["UPDATE:CUSTOMERS"])):
    """
    Update customer information.
    
    Args:
        id: Customer ID to update
        customer_data: Updated customer data
        db: Database session
        payload: Validated token payload
        
    Returns:
        CustomerResponse: Updated customer information
    """
    return await user.update_customer(id, customer_data, db, payload)

@router.delete("/{id}", response_class=JSONResponse)
async def delete_customer(id: str, db: Session = Depends(get_postgres_db), payload = Security(validate_token, scopes=["DELETE:CUSTOMERS"])):
    """
    Delete a customer account.
    
    Args:
        id: Customer ID to delete
        db: Database session
        payload: Validated token payload
        
    Returns:
        JSONResponse: Success message
    """
    return await user.delete_customer(id, db, payload)