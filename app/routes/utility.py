from fastapi import APIRouter, Depends, Security
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession as Session
from typing import List
from app.database.dependencies import get_postgres_db
from app.models import Status, Timeslot
from app.schemas import StatusCreate, StatusResponse, StatusUpdate, TimeslotCreate, TimeslotResponse, TimeslotUpdate
from app.services import crud
from app.auth.dependencies import validate_token

router = APIRouter()

# status table
@router.get("/status", response_model=List[StatusResponse])
async def get_status(db: Session = Depends(get_postgres_db), payload = Security(validate_token, scopes=["READ:UTILS"])):
    return await crud.get_all_records(db, Status)

@router.post("/status", response_model=StatusResponse)
async def create_status(status: StatusCreate, db: Session = Depends(get_postgres_db), payload = Security(validate_token, scopes=["WRITE:UTILS"])):
    return await crud.create_record(db, status.model_dump(), Status)

@router.put("/status/{id}", response_model=StatusResponse)
async def update_status_by_id(id: int, status: StatusUpdate, db: Session = Depends(get_postgres_db), payload = Security(validate_token, scopes=["UPDATE:UTILS"])):
    return await crud.update_record_by_primary_key(db, id, status.model_dump(exclude_none=True), Status)

@router.delete("/status/{id}", response_class=JSONResponse)
async def delete_status_by_id(id: int, db: Session = Depends(get_postgres_db), payload = Security(validate_token, scopes=["DELETE:UTILS"])):
    message = await crud.delete_record_by_primary_key(db, id, Status)
    return JSONResponse(content=message)


# timeslots table
@router.get("/timeslot", response_model=List[TimeslotResponse])
async def get_timeslots(db: Session = Depends(get_postgres_db), payload = Security(validate_token, scopes=["READ:UTILS"])):
    return await crud.get_all_records(db, Timeslot)

@router.post("/timeslot", response_model=TimeslotResponse)
async def create_timeslot(timeslot: TimeslotCreate, db: Session = Depends(get_postgres_db), payload = Security(validate_token, scopes=["WRITE:UTILS"])):
    return await crud.create_record(db, timeslot.model_dump(), Timeslot)

@router.put("/timeslot/{id}", response_model=TimeslotResponse)
async def update_timeslot_by_id(id: int, timeslot: TimeslotUpdate, db: Session = Depends(get_postgres_db), payload = Security(validate_token, scopes=["UPDATE:UTILS"])):
    return await crud.update_record_by_primary_key(db, id, timeslot.model_dump(exclude_none=True), Timeslot)

@router.delete("/timeslot/{id}", response_class=JSONResponse)
async def delete_timeslot_by_id(id: int, db: Session = Depends(get_postgres_db), payload = Security(validate_token, scopes=["DELETE:UTILS"])):
    message = await crud.delete_record_by_primary_key(db, id, Timeslot)
    return JSONResponse(content=message)