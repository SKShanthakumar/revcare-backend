from fastapi import APIRouter, Depends, Security, HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy import select, desc
from sqlalchemy.ext.asyncio import AsyncSession as Session
from sqlalchemy.orm import selectinload
from typing import List, Optional

from app.database.dependencies import get_postgres_db
from app.models import NotificationLog
from app.schemas import NotificationLogResponse
from app.services.notification import send_query_response
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
    Get notification logs with optional filters
    Admin can view all logs, or filter by customer/status/type
    """
    query = select(NotificationLog).options(
        selectinload(NotificationLog.category),
    ).order_by(desc(NotificationLog.timestamp))
    
    if notification_category:
        query = query.where(NotificationLog.notification_category_id == notification_category)
    
    query = query.limit(limit)
    
    result = await db.execute(query)
    return result.scalars().all()


# Test Email Endpoint (for development/testing)
@router.post("/test-email", response_class=JSONResponse)
async def test_email(
    email: str,
    notification_type: str = "query_response",
    db: Session = Depends(get_postgres_db),
    payload = Security(validate_token, scopes=["WRITE:QUERIES"])
):
    """
    Send a test email (for testing purposes)
    notification_type: 'query_response', 'booking_confirmation', 'progress_update', 'invoice'
    """
    try:
        if notification_type == "query_response":
            await send_query_response(
                db=db,
                query_email=email,
                query_text="This is a test query to check email functionality",
                response_text="This is a test response. If you received this email, the notification system is working correctly!",
                admin_name="Test Admin"
            )
        else:
            raise HTTPException(status_code=400, detail=f"Test not implemented for type: {notification_type}")
        
        return JSONResponse(content={
            "message": f"Test email sent successfully to {email}",
            "type": notification_type
        })
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to send test email: {str(e)}")