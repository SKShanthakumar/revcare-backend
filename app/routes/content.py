from fastapi import APIRouter, Depends, Security
from app.database.dependencies import get_mongo_db
from app.auth.dependencies import validate_token
from app.models.content import Content
from app.services.content import get_content_by_content_id, update_content_bulk, get_contents
from app.schemas import ContentUpdateResponse, ContentResposne
from typing import Dict, List
from motor.motor_asyncio import AsyncIOMotorDatabase

router = APIRouter()

@router.get("/", response_model=List[ContentResposne])
async def get_content_by_id(
    db: AsyncIOMotorDatabase = Depends(get_mongo_db),
) -> Content:
    """
    Retrieve all content.

    Args:
        db (AsyncIOMotorDatabase): MongoDB database connection.

    Returns:
        List[Content]: The content records found.
    """
    return await get_contents(db)


@router.put("/", response_model=List[ContentUpdateResponse])
async def update_content(
    updates: Dict[str, str],
    payload: dict = Security(validate_token, scopes=["UPDATE:CONTENT"]),
    db: AsyncIOMotorDatabase = Depends(get_mongo_db),
) -> List[ContentUpdateResponse]:
    """
    Update multiple content records.

    Args:
        updates (Dict[str, str]): Dictionary mapping `content_id` to new data.
            Example:
            {
                "home_banner": "https://cdn.example.com/new_banner.png",
                "about_us": "Updated about us text"
            }
        payload (dict): Auth token payload from JWT validation.
        db (AsyncIOMotorDatabase): MongoDB database connection.

    Returns:
        List[ContentUpdateResponse]: A list of update results showing which
        content IDs were updated or created.
    """
    return await update_content_bulk(db, updates, payload)


@router.get("/{content_id}", response_model=Content)
async def get_content_by_id(
    content_id: str,
    db: AsyncIOMotorDatabase = Depends(get_mongo_db),
) -> Content:
    """
    Retrieve a content record by its unique `content_id`.

    Args:
        content_id (str): The unique content identifier (e.g., 'home_banner').
        db (AsyncIOMotorDatabase): MongoDB database connection.

    Returns:
        Content: The content record if found.
    """
    return await get_content_by_content_id(db, content_id)
