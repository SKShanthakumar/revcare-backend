from datetime import datetime
from fastapi import HTTPException
from datetime import datetime

async def update_gst(db, new_percent: str, payload: dict):
    """
    Update (or create) the single GST record in the database.

    Args:
        db: Database session or Motor client.
        new_percent (str): New GST percentage (e.g., "18%").
        payload (dict): Contains metadata like {"user_id": "admin123"}.

    Returns:
        dict: Information about the update result.
    """
    result = await db.gst.update_one(
        {},  # Empty filter — because only one GST record exists
        {
            "$set": {
                "percent": new_percent,
                "updated_by": payload.get("user_id"),
                "updated_at": datetime.utcnow(),
            }
        },
        upsert=True,
    )

    status = "updated" if result.matched_count else "created"

    return {
        "status": status,
        "updated_percent": new_percent
    }