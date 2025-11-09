from fastapi import APIRouter, Depends, Security, HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession as Session
from typing import List, Optional
from app.database.dependencies import get_postgres_db
from app.models import Area, Address
from app.schemas import AreaCreate, AreaResponse, AreaUpdate, AddressCreate, AddressResponse, AddressUpdate
from app.services import crud, address as address_service
from app.auth.dependencies import validate_token

router = APIRouter()

# area routes
@router.get("/area", response_model=List[AreaResponse])
async def get_areas(db: Session = Depends(get_postgres_db), payload = Security(validate_token, scopes=["READ:AREAS"])):
    """
    Get all areas.
    
    Args:
        db: Database session
        payload: Validated token payload
        
    Returns:
        List[AreaResponse]: List of areas
    """
    return await crud.get_all_records(db, Area)

@router.post("/area", response_model=AreaResponse)
async def create_area(area: AreaCreate, db: Session = Depends(get_postgres_db), payload = Security(validate_token, scopes=["WRITE:AREAS"])):
    """
    Create a new area.
    
    Args:
        area: Area creation data
        db: Database session
        payload: Validated token payload
        
    Returns:
        AreaResponse: Created area
    """
    return await crud.create_record(db, area.model_dump(), Area)

@router.put("/area/{id}", response_model=AreaResponse)
async def update_area_by_id(id: int, area: AreaUpdate, db: Session = Depends(get_postgres_db), payload = Security(validate_token, scopes=["UPDATE:AREAS"])):
    """
    Update an area.
    
    Args:
        id: Area ID
        area: Updated area data
        db: Database session
        payload: Validated token payload
        
    Returns:
        AreaResponse: Updated area
    """
    return await crud.update_record_by_primary_key(db, id, area.model_dump(exclude_none=True), Area)

@router.delete("/area/{id}", response_class=JSONResponse)
async def delete_area_by_id(id: int, db: Session = Depends(get_postgres_db), payload = Security(validate_token, scopes=["DELETE:AREAS"])):
    """
    Delete an area.
    
    Args:
        id: Area ID
        db: Database session
        payload: Validated token payload
        
    Returns:
        JSONResponse: Success message
    """
    message = await crud.delete_record_by_primary_key(db, id, Area)
    return JSONResponse(content=message)


# address routes
@router.get("/", response_model=List[AddressResponse])
async def get_customer_addresses(customer_id: Optional[str] = None, db: Session = Depends(get_postgres_db), payload = Security(validate_token, scopes=["READ:ADDRESSES"])):
    """
    Get customer addresses.
    
    Args:
        customer_id: Optional customer ID to filter by
        db: Database session
        payload: Validated token payload
        
    Returns:
        List[AddressResponse]: List of addresses
    """
    return await address_service.get_customer_address(db, payload, customer_id)

@router.post("/", response_model=AddressResponse)
async def create_address(address: AddressCreate, db: Session = Depends(get_postgres_db), payload = Security(validate_token, scopes=["WRITE:ADDRESSES"])):
    """
    Create a new address.
    
    Args:
        address: Address creation data
        db: Database session
        payload: Validated token payload
        
    Returns:
        AddressResponse: Created address
    """
    return await address_service.create_customer_address(db, payload, address)

@router.put("/{id}", response_model=AddressResponse)
async def update_address_by_id(id: int, address: AddressUpdate, db: Session = Depends(get_postgres_db), payload = Security(validate_token, scopes=["UPDATE:ADDRESSES"])):
    """
    Update an address.
    
    Args:
        id: Address ID
        address: Updated address data
        db: Database session
        payload: Validated token payload
        
    Returns:
        AddressResponse: Updated address
    """
    return await address_service.update_customer_address(db, payload, id, address.model_dump(exclude_none=True))

@router.delete("/{id}", response_class=JSONResponse)
async def delete_address_by_id(id: int, db: Session = Depends(get_postgres_db), payload = Security(validate_token, scopes=["DELETE:ADDRESSES"])):
    """
    Delete an address.
    
    Args:
        id: Address ID
        db: Database session
        payload: Validated token payload
        
    Returns:
        JSONResponse: Success message
    """
    message = await address_service.delete_customer_address(db, payload, id)
    return JSONResponse(content=message)
