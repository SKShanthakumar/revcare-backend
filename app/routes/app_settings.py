from fastapi import APIRouter, Depends, Security
from fastapi.responses import JSONResponse
from app.database.dependencies import get_mongo_db
from app.auth.dependencies import validate_token
from app.services import app_settings
from motor.motor_asyncio import AsyncIOMotorDatabase

router = APIRouter()


@router.put("/validation_automation", response_class=JSONResponse)
async def update_validation_automation_status(
    state: bool,
    payload: dict = Security(validate_token, scopes=["UPDATE:GST"]),
    db: AsyncIOMotorDatabase = Depends(get_mongo_db)
):
    """
    Update Booking Progress' validation is automated or manual.
    
    Args:
        state: True for automated, False for manual
        payload: Validated token payload
        db: MongoDB database session
        
    Returns:
        JSONResponse: Success message
    """
    return await app_settings.toggle_validation_automation_state(db, state, payload)


@router.put("/analysis_validation_automation", response_class=JSONResponse)
async def update_analysis_validation_automation_status(
    state: bool,
    payload: dict = Security(validate_token, scopes=["UPDATE:GST"]),
    db: AsyncIOMotorDatabase = Depends(get_mongo_db)
):
    """
    Update Booking Analysis' validation is automated or manual.
    
    Args:
        state: True for automated, False for manual
        payload: Validated token payload
        db: MongoDB database session
        
    Returns:
        JSONResponse: Success message
    """
    return await app_settings.toggle_analysis_validation_automation_state(db, state, payload)
