from datetime import datetime
from fastapi.responses import JSONResponse

async def toggle_validation_automation_state(db, state: bool, payload: dict):
    """
    Toggle the validation automation state for Booking Progress.

    Args:
        db: Database session or Motor client.
        state (bool): True for automated, False for manual.

    Returns:
        JSONResponse: Confirmation message of the update.
    """
    await db.app_settings.update_one(
        {"setting_id": "validation_automation"},
        {
            "$set": {
                "state": state,
                "updated_by": payload.get("user_id"),
                "updated_at": datetime.utcnow(),
            }
        },
        upsert=True,
    )

    return JSONResponse(content={
        "message": f"Automation state set {state} successfully"
    })


async def toggle_analysis_validation_automation_state(db, state: bool, payload: dict):
    """
    Toggle the validation automation state for Booking Progress.

    Args:
        db: Database session or Motor client.
        state (bool): True for automated, False for manual.

    Returns:
        JSONResponse: Confirmation message of the update.
    """
    await db.app_settings.update_one(
        {"setting_id": "analysis_validation_automation"},
        {
            "$set": {
                "state": state,
                "updated_by": payload.get("user_id"),
                "updated_at": datetime.utcnow(),
            }
        },
        upsert=True,
    )

    return JSONResponse(content={
        "message": f"Automation state set {state} successfully"
    })