from datetime import datetime
from app.models import Content
from fastapi import HTTPException

async def get_content_by_content_id(db, content_id: str):
    """
    Fetch a content document by its content_id.
    
    Args:
        db: MongoDB database session
        content_id: Unique content identifier (e.g., 'home_banner')
        
    Returns:
        Content: Content document
        
    Raises:
        HTTPException: 404 if content is not found
    """
    content = await db.content.find_one({"content_id": content_id})
    if not content:
        raise HTTPException(status_code=404, detail="Content not found")
    return Content(**content)


async def get_contents(db):
    """
    Fetch all content documents.
    
    Args:
        db: MongoDB database session
        
    Returns:
        List[Content]: List of all Content document
        
    """
    contents = db.content.find()
    return [
        {
            "content_id": item["content_id"],
            "data": item["data"]
        }
        async for item in contents
    ]


async def update_content_bulk(db, updates: dict, payload: dict):
    """
    Update multiple content items by content_id.
    
    Updates or creates content items based on content_id. Creates new items
    if they don't exist (upsert).
    
    Args:
        db: MongoDB database session
        updates: Dictionary mapping content_id to new data
                 Example: {"home_banner": "https://cdn.site.com/new_banner.png"}
        payload: Token payload containing user_id
        
    Returns:
        list: List of update results with content_id and status
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
