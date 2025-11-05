from fastapi import APIRouter, Depends, Security, HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession as Session
from typing import List
from app.database.dependencies import get_postgres_db
from app.models import Admin
from app.schemas import AdminCreate, AdminResponse, AdminUpdate
from app.services import user, crud, admin as admin_service
from app.auth.dependencies import validate_token

router = APIRouter()

@router.get("/", response_model=List[AdminResponse])
async def get_all_admins(db: Session = Depends(get_postgres_db), payload = Security(validate_token, scopes=["READ:ADMINS"])):
    return await crud.get_all_records(db, Admin)

@router.post("/", response_model=AdminResponse)
async def create_admin(admin: AdminCreate, db: Session = Depends(get_postgres_db), payload = Security(validate_token, scopes=["WRITE:ADMINS"])):
    return await user.create_user(db, admin, Admin)
    
@router.get("/{id}", response_model=AdminResponse)
async def get_admin_by_id(id: str, db: Session = Depends(get_postgres_db), payload = Security(validate_token, scopes=["READ:ADMINS"])):
    return await crud.get_record_by_primary_key(db, id.strip(), Admin)

@router.put("/{id}", response_model=AdminResponse)
async def update_admin(id: str, admin_data: AdminUpdate, db: Session = Depends(get_postgres_db), payload = Security(validate_token, scopes=["UPDATE:ADMINS"])):
    return await admin_service.update_admin(db, payload, id, admin_data)

@router.delete("/{id}", response_class=JSONResponse)
async def delete_admin(id: str, db: Session = Depends(get_postgres_db), payload = Security(validate_token, scopes=["DELETE:ADMINS"])):
    return await admin_service.delete_admin(db, payload, id)