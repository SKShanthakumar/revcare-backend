from fastapi import APIRouter, Form, Depends, Request
from sqlalchemy.ext.asyncio import AsyncSession as Session
from pathlib import Path
from app.database.dependencies import get_postgres_db
from app.services import bookings as booking_service

router = APIRouter()


@router.post("/verify")
async def verify_payment(
    razorpay_payment_id: str = Form(...),
    razorpay_order_id: str = Form(...),
    razorpay_signature: str = Form(...),
    db: Session = Depends(get_postgres_db)
):  
    return booking_service.confirm_booking_webhook(db, razorpay_order_id, razorpay_payment_id, razorpay_signature)
