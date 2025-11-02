from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession as Session
from app.models import Address
from app.services import crud

async def update_customer_address(db: Session, payload: dict, address_id: int, new_data: dict):
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
    # check customer trying to access other customer's address - if condition also bypasses admin
    if payload.get("role") == 3:
        address = await db.get(Address, address_id)
        if address is None:
            raise HTTPException(status_code=403, detail="Address not found.")
        customer_id = payload.get("user_id")
        if address.customer_id != customer_id:
            raise HTTPException(status_code=403, detail="Operation not permitted. Trying to access addresses of other customers.")
        
    return await crud.delete_record_by_primary_key(db, address_id, Address)
