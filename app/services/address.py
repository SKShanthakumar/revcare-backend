from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession as Session
from app.models import Address
from app.services import crud
from app.schemas import AddressCreate

async def get_customer_address(db: Session, payload: dict, customer_id: str):
    """
    Get customer address(es) with access control.
    
    If customer_id is provided, returns addresses for that customer (with permission check).
    Otherwise, returns addresses for the logged-in customer.
    
    Args:
        db: Async database session
        payload: Token payload containing user_id and role
        customer_id: Optional customer ID to filter by
        
    Returns:
        list: List of Address instances
        
    Raises:
        HTTPException: 403 if customer tries to access another customer's addresses
    """
    filters = None
    if customer_id is not None:
        if payload.get("role") == 3 and (customer_id != payload.get("user_id")):
            raise HTTPException(status_code=403, detail="Operation not permitted. Trying to access addresses of other customers.")
        
        filters = {"customer_id": customer_id}
    else:
        user_id = payload.get("user_id")
        if user_id.startswith("CST"):
            filters = {"customer_id": user_id}

    return await crud.get_all_records(db, Address, filters=filters)


async def create_customer_address(db: Session, payload: dict, address: AddressCreate):
    """
    Create a new address for a customer.
    
    Args:
        db: Async database session
        payload: Token payload containing user_id
        address: Address creation data
        
    Returns:
        Address: Created address instance
        
    Raises:
        HTTPException: 403 if user is not a customer
    """
    customer_id = payload.get("user_id")
    
    if not customer_id.startswith("CST"):
        raise HTTPException(status_code=403, detail="Operation not permitted. Only Customers can add addresses")
    
    address_dict = address.model_dump()
    address_dict["customer_id"] = customer_id

    return await crud.create_record(db, address_dict, Address)


async def update_customer_address(db: Session, payload: dict, address_id: int, new_data: dict):
    """
    Update a customer address.
    
    Enforces access control - customers can only update their own addresses.
    Admins can update any address.
    
    Args:
        db: Async database session
        payload: Token payload containing user_id and role
        address_id: Address ID to update
        new_data: Updated address data
        
    Returns:
        Address: Updated address instance
        
    Raises:
        HTTPException: 
            - 403 if customer tries to update another customer's address
            - 403 if address is not found
    """
    # check customer trying to access other customer's address - if condition also bypasses admin
    if payload.get("role") == 3:
        address = await db.get(Address, address_id)
        if address is None:
            raise HTTPException(status_code=403, detail="Address not found.")
        customer_id = payload.get("user_id")
        if address.customer_id != customer_id:
            raise HTTPException(status_code=403, detail="Operation not permitted. Trying to access addresses of other customers.")
        
    return await crud.update_record_by_primary_key(db, address_id, new_data, Address)


async def delete_customer_address(db: Session, payload: dict, address_id: int):
    """
    Delete a customer address.
    
    Enforces access control - customers can only delete their own addresses.
    Admins can delete any address.
    
    Args:
        db: Async database session
        payload: Token payload containing user_id and role
        address_id: Address ID to delete
        
    Returns:
        dict: Success message
        
    Raises:
        HTTPException: 
            - 403 if customer tries to delete another customer's address
            - 403 if address is not found
    """
    # check customer trying to access other customer's address - if condition also bypasses admin
    if payload.get("role") == 3:
        address = await db.get(Address, address_id)
        if address is None:
            raise HTTPException(status_code=403, detail="Address not found.")
        customer_id = payload.get("user_id")
        if address.customer_id != customer_id:
            raise HTTPException(status_code=403, detail="Operation not permitted. Trying to access addresses of other customers.")
        
    return await crud.delete_record_by_primary_key(db, address_id, Address)
