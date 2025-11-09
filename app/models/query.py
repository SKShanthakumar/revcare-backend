from pydantic import Field
from typing import Optional
from datetime import datetime
from app.database.utils import PyObjectId
from app.core.config import BaseModelWithObjectId

class Query(BaseModelWithObjectId):
    id: Optional[PyObjectId] = Field(default_factory=PyObjectId, alias="_id")
    customer_email: str = Field(..., description="Email address of the customer")
    query: str = Field(..., description="Customer question")
    response: Optional[str] = Field(None, description="Response from admin")
    responded_by: Optional[str] = Field(None, description="Admin ID who responded")
    created_at: datetime = Field(default_factory=datetime.utcnow)
    responded_at: Optional[datetime] = None
