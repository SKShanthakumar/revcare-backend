from fastapi import APIRouter, Depends, Security, HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession as Session
from typing import List
from app.database.dependencies import get_postgres_db
from app.models import Mechanic
from app.schemas import MechanicCreate, MechanicResponse, MechanicUpdate
from app.services import user
from app.auth.dependencies import validate_token

router = APIRouter()

@router.get("/", response_model=List[MechanicResponse])
async def get_all_mechanics(db: Session = Depends(get_postgres_db), payload = Security(validate_token, scopes=["READ:MECHANICS"])):
    return await user.get_all_users(db, Mechanic)

@router.post("/", response_model=MechanicResponse)
async def create_mechanic(mechanic: MechanicCreate, db: Session = Depends(get_postgres_db), payload = Security(validate_token, scopes=["WRITE:MECHANICS"])):
    return await user.create_user(db, mechanic, Mechanic)
    
@router.get("/{id}", response_model=MechanicResponse)
async def get_mechanic_by_id(id: str, db: Session = Depends(get_postgres_db), payload = Security(validate_token, scopes=["READ:MECHANICS"])):
    return await user.get_user_by_id(db, id.strip(), Mechanic)

@router.put("/{id}", response_model=MechanicResponse)
async def update_mechanic(id: str, mechanic_data: MechanicUpdate, db: Session = Depends(get_postgres_db), payload = Security(validate_token, scopes=["UPDATE:MECHANICS"])):
    if payload.get("role") != 1 and payload.get("user_id") != id:
        raise HTTPException(status_code=403, detail="Operation not permitted.")
    
    return await user.update_user(db, id.strip(), mechanic_data, Mechanic)

@router.delete("/{id}", response_class=JSONResponse)
async def delete_mechanic(id: str, db: Session = Depends(get_postgres_db), payload = Security(validate_token, scopes=["DELETE:MECHANICS"])):
    if payload.get("role") != 1 and payload.get("user_id") != id:
        raise HTTPException(status_code=403, detail="Operation not permitted.")
    
    message = await user.delete_user(db, id.strip(), Mechanic)
    return JSONResponse(content=message)