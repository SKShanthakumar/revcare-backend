from fastapi import APIRouter, Depends, Security, HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession as Session
from typing import List, Optional
from app.database.dependencies import get_postgres_db
from app.models import Mechanic, AssignmentType
from app.schemas import MechanicCreate, MechanicResponse, MechanicUpdateWithForeignData, AssignmentTypeCreate, AssignmentTypeResponse, AssignmentTypeUpdate
from app.services import user, crud
from app.auth.dependencies import validate_token

router = APIRouter()

# assigment type utils routes
@router.get("/assignment_type", response_model=List[AssignmentTypeResponse])
async def get_assignment_types(db: Session = Depends(get_postgres_db), payload = Security(validate_token, scopes=["READ:UTILS"])):
    return await crud.get_all_records(db, AssignmentType)

@router.post("/assignment_type", response_model=AssignmentTypeResponse)
async def create_assignment_type(assignment_type: AssignmentTypeCreate, db: Session = Depends(get_postgres_db), payload = Security(validate_token, scopes=["WRITE:UTILS"])):
    return await crud.create_record(db, assignment_type.model_dump(), AssignmentType)

@router.put("/assignment_type/{id}", response_model=AssignmentTypeResponse)
async def update_assignment_type_by_id(id: int, assignment_type: AssignmentTypeUpdate, db: Session = Depends(get_postgres_db), payload = Security(validate_token, scopes=["UPDATE:UTILS"])):
    return await crud.update_record_by_primary_key(db, id, assignment_type.model_dump(exclude_none=True), AssignmentType)

@router.delete("/assignment_type/{id}", response_class=JSONResponse)
async def delete_assignment_type_by_id(id: int, db: Session = Depends(get_postgres_db), payload = Security(validate_token, scopes=["DELETE:UTILS"])):
    message = await crud.delete_record_by_primary_key(db, id, AssignmentType)
    return JSONResponse(content=message)


# crud routes
@router.get("/", response_model=List[MechanicResponse])
async def get_all_mechanics(mechanic_id: Optional[str] = None, db: Session = Depends(get_postgres_db), payload = Security(validate_token, scopes=["READ:MECHANICS"])):
    return await user.get_mechanics(db, payload, mechanic_id)

@router.post("/", response_model=MechanicResponse)
async def create_mechanic(mechanic: MechanicCreate, db: Session = Depends(get_postgres_db), payload = Security(validate_token, scopes=["WRITE:MECHANICS"])):
    return await user.create_mechanic(db, mechanic)

@router.put("/{id}", response_model=MechanicResponse)
async def update_mechanic(id: str, mechanic_data: MechanicUpdateWithForeignData, db: Session = Depends(get_postgres_db), payload = Security(validate_token, scopes=["UPDATE:MECHANICS"])):
    return await user.update_mechanic(db, id, mechanic_data, payload)

@router.delete("/{id}", response_class=JSONResponse)
async def delete_mechanic(id: str, db: Session = Depends(get_postgres_db), payload = Security(validate_token, scopes=["DELETE:MECHANICS"])):
    return await user.delete_mechanic(id, db, payload)