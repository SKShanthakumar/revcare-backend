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
    """
    Verify and process Razorpay payment for booking service selection.
    
    Webhook endpoint for Razorpay to verify payment and confirm service selection.
    
    Args:
        razorpay_payment_id: Razorpay payment ID
        razorpay_order_id: Razorpay order ID
        razorpay_signature: Razorpay payment signature
        db: Database session
        
    Returns:
        JSONResponse: Payment verification result
    """
    return await booking_service.confirm_booking_webhook(db, razorpay_order_id, razorpay_payment_id, razorpay_signature)

@router.post("/cash-on-delivery/{booking_id}", response_class=JSONResponse)
async def process_cash_on_delivery(
    booking_id: int,
    request_body: CashOnDelivery,
    db: Session = Depends(get_postgres_db),
    payload = Security(validate_token, scopes=[])
):
    """
    Process cash on delivery payment for a booking.
    
    Args:
        booking_id: Booking ID
        request_body: Cash on delivery data with payment method
        db: Database session
        payload: Validated token payload
        
    Returns:
        JSONResponse: Payment order details or success message
    """
    return await booking_service.receive_cash_on_delivery(db, booking_id, request_body, payload)

@router.post("/verify-cod")
async def verify_cash_on_delivery_payment(
    razorpay_payment_id: str = Form(...),
    razorpay_order_id: str = Form(...),
    razorpay_signature: str = Form(...),
    db: Session = Depends(get_postgres_db)
):
    """
    Verify and process Razorpay payment for cash on delivery.
    
    Webhook endpoint for Razorpay to verify COD payment made at delivery time.
    
    Args:
        razorpay_payment_id: Razorpay payment ID
        razorpay_order_id: Razorpay order ID
        razorpay_signature: Razorpay payment signature
        db: Database session
        
    Returns:
        JSONResponse: Payment verification result
    """
    return await booking_service.confirm_payment_webhook(db, razorpay_order_id, razorpay_payment_id, razorpay_signature)
