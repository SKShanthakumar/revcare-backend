from datetime import datetime
from app.models import Content
from fastapi import HTTPException

async def get_content_by_content_id(db, content_id: str):
    """Fetch a content document by its content_id."""
    content = await db.content.find_one({"content_id": content_id})
    if not content:
        raise HTTPException(status_code=404, detail="Content not found")
    return Content(**content)


async def update_content_bulk(db, updates: dict, payload: dict):
    """
    Update multiple content items by content_id.
    Body example:
    {
        "home_banner": "https://cdn.site.com/new_banner.png",
        "about_text": "Welcome to our platform!"
    }
    """
    results = []

    for content_id, new_data in updates.items():
        result = await db.content.update_one(
            {"content_id": content_id},
            {
                "$set": {
                    "data": new_data,
                    "updated_by": payload.get("user_id"),
                    "updated_at": datetime.utcnow(),
                }
            },
            upsert=True,
        )

        results.append({
            "content_id": content_id,
            "status": "updated" if result.modified_count else "created"
        })

    return results
