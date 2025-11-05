from fastapi import HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession as Session
from app.models import Admin
from app.services import crud
from app.schemas import AdminUpdate

async def update_admin(db: Session, payload: dict, id: str, admin_data: AdminUpdate):
    if payload.get("role") != 1 and payload.get("user_id") != id:
        raise HTTPException(status_code=403, detail="Operation not permitted.")
    
    return await crud.update_record_by_primary_key(db, id.strip(), admin_data.model_dump(exclude_none=True), Admin)

async def delete_admin(db: Session, payload: dict, id: str):
    if payload.get("role") != 1 and payload.get("user_id") != id:
        raise HTTPException(status_code=403, detail="Operation not permitted.")
    
    message = await crud.delete_record_by_primary_key(db, id.strip(), Admin)
    return JSONResponse(content=message)