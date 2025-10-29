from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from typing import List
from app.database.dependencies import get_postgres_db
from app.models import Mechanic
from app.schemas import MechanicCreate, MechanicResponse, MechanicUpdate
from app.services import user

router = APIRouter()

@router.get("/", response_model=List[MechanicResponse])
def get_all_mechanics(db: Session = Depends(get_postgres_db)):
    return user.get_all_users(db, Mechanic)

@router.post("/", response_model=MechanicResponse)
def create_mechanic(mechanic: MechanicCreate, db: Session = Depends(get_postgres_db)):
    return user.create_user(db, mechanic, Mechanic)
    
@router.get("/{id}", response_model=MechanicResponse)
def get_mechanic_by_id(id: str, db: Session = Depends(get_postgres_db)):
    return user.get_user_by_id(db, id.strip(), Mechanic)

@router.put("/{id}", response_model=MechanicResponse)
def update_mechanic(id: str, mechanic_data: MechanicUpdate, db: Session = Depends(get_postgres_db)):
    return user.update_user(db, id.strip(), mechanic_data, Mechanic)

@router.delete("/{id}", response_class=JSONResponse)
def delete_mechanic(id: str, db: Session = Depends(get_postgres_db)):
    message = user.delete_user(db, id.strip(), Mechanic)
    return JSONResponse(content=message)