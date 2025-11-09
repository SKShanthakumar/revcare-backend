from pydantic import BaseModel, EmailStr
from typing import List
from datetime import datetime


class QueryCreate(BaseModel):
    customer_email: str
    query_text: str

class QueryResponse(BaseModel):
    response: str

class NotificationLogResponse(BaseModel):
    id: int
    notification_category_id: int
    recipient_email: EmailStr
    subject: str
    attachments: List[str]
    timestamp: datetime
    
    class Config:
        from_attributes = True