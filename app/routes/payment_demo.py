from fastapi import APIRouter, Depends, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession as Session
from app.database.dependencies import get_postgres_db
from app.core.config import settings
from app.models import OfflinePayment


router = APIRouter()
templates = Jinja2Templates(directory="app/templates")

@router.get("/confirm_booking/{booking_id}", response_class=HTMLResponse)
async def render_confirm_service_page(request: Request, booking_id: int, access_token: str):
    """
    Render payment confirmation page for booking service selection.
    
    Args:
        request: FastAPI Request object
        booking_id: Booking ID
        access_token: JWT access token for authenticated requests
        
    Returns:
        HTMLResponse: Rendered HTML page for payment confirmation
    """
    print(access_token)
    return templates.TemplateResponse(
        "confirm_booking.html",
        {
            "request": request,
            "booking_id": booking_id,
            "access_token": access_token,
            "key_id": settings.razorpay_key_id
        }
    )

from app.database.dependencies import get_postgres_db

@router.get("/cash_on_delivery/{booking_id}")
async def render_cod_page(request: Request, booking_id: int, access_token: str, db: Session = Depends(get_postgres_db)):
    """
    Render cash on delivery payment page.
    
    Args:
        request: FastAPI Request object
        booking_id: Booking ID
        access_token: JWT access token for authenticated requests
        db: Database session
        
    Returns:
        HTMLResponse: Rendered HTML page for cash on delivery payment
    """
    result = await db.execute(select(OfflinePayment).where(OfflinePayment.booking_id == booking_id))
    payment_obj = result.scalar_one_or_none()
    
    total_with_gst = None
    if payment_obj:
        total_price = payment_obj.amount

        # Add GST
        gst_amount = payment_obj.gst
        total_with_gst = total_price + gst_amount

    return templates.TemplateResponse(
        "cash_on_delivery.html",
        {
            "request": request,
            "booking_id": booking_id,
            "amount": total_with_gst,
            "access_token": access_token,
            "key_id": settings.razorpay_key_id
        }
    )