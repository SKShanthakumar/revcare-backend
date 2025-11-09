from fastapi import APIRouter, Depends, Security
from app.database.dependencies import get_mongo_db
from app.auth.dependencies import validate_token
from app.schemas import GstResponse
from app.services import gst
from motor.motor_asyncio import AsyncIOMotorDatabase

router = APIRouter()


@router.put("/", response_model=GstResponse)
async def update_gst(
    percent: int,
    payload: dict = Security(validate_token, scopes=["UPDATE:GST"]),
    db: AsyncIOMotorDatabase = Depends(get_mongo_db)
):
    """Get content by its unique content_id."""
    return await gst.update_gst(db, percent, payload)
