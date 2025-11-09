from fastapi import APIRouter, Depends, Security, HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy import select, desc
from sqlalchemy.ext.asyncio import AsyncSession as Session
from sqlalchemy.orm import selectinload
from typing import List, Optional

from app.database.dependencies import get_postgres_db
from app.models import NotificationLog
from app.schemas import NotificationLogResponse
from app.services import notification as notification_service
from app.auth.dependencies import validate_token

router = APIRouter()


# Notification Log Endpoints
@router.get("/notifications/logs", response_model=List[NotificationLogResponse])
async def get_notification_logs(
    notification_category: Optional[int] = None,  # 'email', 'sms', 'whatsapp'
    limit: int = 100,
    db: Session = Depends(get_postgres_db),
    payload = Security(validate_token, scopes=["READ:NOTIFICATION_LOG"])
):
    """
    Get notification logs with optional filters.
    
    Admin can view all logs, or filter by notification category and limit results.
    
    Args:
        notification_category: Optional notification category ID to filter by
        limit: Maximum number of logs to return (default: 100)
        db: Database session
        payload: Validated token payload
        
    Returns:
        List[NotificationLogResponse]: List of notification logs
    """
    return await notification_service.get_notification_logs(db, notification_category, limit)