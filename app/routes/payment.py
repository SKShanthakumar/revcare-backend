from fastapi import APIRouter, Form, Depends, Security
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession as Session
from app.database.dependencies import get_postgres_db
from app.services import bookings as booking_service
from app.auth.dependencies import validate_token
from app.schemas import CashOnDelivery

router = APIRouter()


@router.post("/verify")
async def verify_payment(
    razorpay_payment_id: str = Form(...),
    razorpay_order_id: str = Form(...),
    razorpay_signature: str = Form(...),
    db: Session = Depends(get_postgres_db)
):  
    return await booking_service.confirm_booking_webhook(db, razorpay_order_id, razorpay_payment_id, razorpay_signature)

@router.post("/cash-on-delivery/{booking_id}", response_class=JSONResponse)
async def process_cash_on_delivery(
    booking_id: int,
    request_body: CashOnDelivery,
    db: Session = Depends(get_postgres_db),
    payload = Security(validate_token, scopes=[])
):
    return await booking_service.receive_cash_on_delivery(db, booking_id, request_body, payload)

@router.post("/verify-cod")
async def verify_cash_on_delivery_payment(
    razorpay_payment_id: str = Form(...),
    razorpay_order_id: str = Form(...),
    razorpay_signature: str = Form(...),
    db: Session = Depends(get_postgres_db)
):
    return await booking_service.confirm_payment_webhook(db, razorpay_order_id, razorpay_payment_id, razorpay_signature)
