from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from typing import List
from app.database.dependencies import get_postgres_db
from app.models import Admin
from app.schemas import AdminCreate, AdminResponse, AdminUpdate
from app.services import user

router = APIRouter()

@router.get("/", response_model=List[AdminResponse])
def get_all_admins(db: Session = Depends(get_postgres_db)):
    return user.get_all_users(db, Admin)

@router.post("/", response_model=AdminResponse)
def create_admin(admin: AdminCreate, db: Session = Depends(get_postgres_db)):
    return user.create_user(db, admin, Admin)
    
@router.get("/{id}", response_model=AdminResponse)
def get_admin_by_id(id: str, db: Session = Depends(get_postgres_db)):
    return user.get_user_by_id(db, id.strip(), Admin)

@router.put("/{id}", response_model=AdminResponse)
def update_admin(id: str, admin_data: AdminUpdate, db: Session = Depends(get_postgres_db)):
    return user.update_user(db, id.strip(), admin_data, Admin)

@router.delete("/{id}", response_class=JSONResponse)
def delete_admin(id: str, db: Session = Depends(get_postgres_db)):
    message = user.delete_user(db, id.strip(), Admin)
    return JSONResponse(content=message)