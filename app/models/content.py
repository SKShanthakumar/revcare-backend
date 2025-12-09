from pydantic import Field
from typing import Optional
from datetime import datetime
from app.database.utils import PyObjectId
from app.core.config import BaseModelWithObjectId


class Content(BaseModelWithObjectId):
    id: Optional[PyObjectId] = Field(default_factory=PyObjectId, alias="_id")
    content_id: str = Field(..., description="Unique content identifier")
    data: str = Field(..., description="Content data or image URL")
    updated_by: Optional[str] = Field(default=None, description="Admin id who updated")
    updated_at: Optional[datetime] = Field(default_factory=datetime.utcnow)
    