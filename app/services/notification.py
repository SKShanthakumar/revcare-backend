from fastapi import HTTPException
from fastapi_mail import FastMail, MessageSchema, MessageType
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession as Session
from sqlalchemy.orm import selectinload
from app.models import Booking, CustomerCar, Car, BookedService, Address
from typing import Optional, Dict, Any, List
from datetime import datetime
from decimal import Decimal

from app.core.config import email_conf
from app.models import (
    Booking, NotificationLog, NotificationCategory, BookingProgress
)


# --------------------------------------------------------
# Notification Type Constants
# --------------------------------------------------------
class NotificationType:
    BOOKING_CONFIRMATION = "booking_confirmation"
    PROGRESS_UPDATE = "progress_update"
    INVOICE = "invoice"
    QUERY_RESPONSE = "query_response"


# --------------------------------------------------------
# Utility: Safe ORM Eager Loading + Serialization
# --------------------------------------------------------
async def fetch_booking_with_relations(db: Session, booking_id: int) -> Booking:
    """Fetch booking with all needed relationships (eager loaded)."""
    result = await db.execute(
        select(Booking)
        .options(
            selectinload(Booking.customer),
            selectinload(Booking.customer_car)
                .selectinload(CustomerCar.car)
                .selectinload(Car.manufacturer),
            selectinload(Booking.booked_services)
                .selectinload(BookedService.service),
            selectinload(Booking.booked_services)
                .selectinload(BookedService.status),
            selectinload(Booking.pickup_address)
                .selectinload(Address.area),
            selectinload(Booking.drop_address)
                .selectinload(Address.area),
            selectinload(Booking.pickup_timeslot),
            selectinload(Booking.drop_timeslot),
            selectinload(Booking.status),
        )
        .where(Booking.id == booking_id)
    )
    booking = result.scalar_one_or_none()
    if not booking:
        raise HTTPException(status_code=404, detail=f"Booking {booking_id} not found")
    return booking

def serialize_booking(booking: Booking) -> Dict[str, Any]:
    """Convert ORM booking object into a plain dict (safe for templates)."""
    return {
        "id": booking.id,
        "customer": {
            "name": booking.customer.name,
            "email": booking.customer.email,
            "phone": booking.customer.phone,
        },
        "car": {
            "model": booking.customer_car.car.model,
            "manufacturer": booking.customer_car.car.manufacturer.name,
        },
        "booked_services": [
            {
                "name": bs.service.title,
                "est_price": float(bs.est_price or 0),
                "price": float(bs.price or 0),
                "status": bs.status.name,
                "completed": bs.completed,
                "warranty_kms": bs.service.warranty_kms,
                "warranty_months": bs.service.warranty_months,
            }
            for bs in booking.booked_services
        ],
        "pickup_date": booking.pickup_date,
        "drop_date": booking.drop_date,
        "pickup_timeslot": booking.pickup_timeslot.name,
        "drop_timeslot": booking.drop_timeslot.name,
        "pickup_address": f"{booking.pickup_address.line1}, {booking.pickup_address.area.name}",
        "drop_address": f"{booking.drop_address.line1}, {booking.drop_address.area.name}",
        "status": booking.status.name,
        "car_reg_number": booking.car_reg_number,
        "created_at": booking.created_at,
        "completed_at": booking.completed_at,
    }


# --------------------------------------------------------
# Notification Category + Logging
# --------------------------------------------------------
async def get_notification_category_id(db: Session, category_name: str) -> int:
    result = await db.execute(
        select(NotificationCategory).where(NotificationCategory.name == category_name)
    )
    category = result.scalar_one_or_none()
    if not category:
        raise HTTPException(status_code=404, detail=f"Notification category '{category_name}' not found")
    return category.id


async def log_notification(
    db: Session,
    category_name: str,
    recipient_email: str,
    subject: str,
    attachments: Optional[List[str]] = None
):
    try:
        category_id = await get_notification_category_id(db, category_name)
        log_entry = NotificationLog(
            notification_category_id=category_id,
            recipient_email=recipient_email,
            subject=subject,
            attachments=attachments or []
        )
        db.add(log_entry)
        await db.commit()
        return log_entry
    except Exception as e:
        await db.rollback()
        print(f"Error logging notification: {str(e)}")
        return None


# --------------------------------------------------------
# Template Data Preparation (All Plain Dicts)
# --------------------------------------------------------
def prepare_booking_confirmation_data(booking: Dict[str, Any]) -> Dict[str, Any]:
    total_price = sum(s["est_price"] for s in booking["booked_services"])
    return {
        "customer_name": booking["customer"]["name"],
        "booking_id": booking["id"],
        "car_model": f"{booking['car']['manufacturer']} {booking['car']['model']}",
        "car_reg": booking["car_reg_number"],
        "pickup_date": booking["pickup_date"].strftime("%B %d, %Y"),
        "pickup_time": booking["pickup_timeslot"],
        "pickup_address": booking["pickup_address"],
        "drop_date": booking["drop_date"].strftime("%B %d, %Y"),
        "drop_time": booking["drop_timeslot"],
        "drop_address": booking["drop_address"],
        "services": booking["booked_services"],
        "total_price": total_price,
        "created_at": booking["created_at"].strftime("%B %d, %Y %I:%M %p")
    }


def prepare_progress_update_data(booking: Dict[str, Any], progress: BookingProgress) -> Dict[str, Any]:
    return {
        "customer_name": booking["customer"]["name"],
        "booking_id": booking["id"],
        "car_model": f"{booking['car']['manufacturer']} {booking['car']['model']}",
        "car_reg": booking["car_reg_number"],
        "status": booking["status"],
        "progress_description": progress.description,
        "update_time": progress.created_at.strftime("%B %d, %Y %I:%M %p"),
        "mechanic_name": progress.mechanic.name if progress.mechanic else "Service Team",
        "images": progress.images or []
    }


def prepare_invoice_data(booking: Dict[str, Any]) -> Dict[str, Any]:
    completed_services = [
        s for s in booking["booked_services"]
        if s["status"].lower() == "confirmed" and s["completed"]
    ]
    subtotal = sum(s["price"] for s in completed_services)
    gst_rate = 0.18
    gst_amount = subtotal * gst_rate
    total = subtotal + gst_amount
    return {
        "customer_name": booking["customer"]["name"],
        "customer_email": booking["customer"]["email"],
        "customer_phone": booking["customer"]["phone"],
        "booking_id": booking["id"],
        "invoice_date": (
            booking["completed_at"].strftime("%B %d, %Y")
            if booking["completed_at"] else datetime.now().strftime("%B %d, %Y")
        ),
        "car_model": f"{booking['car']['manufacturer']} {booking['car']['model']}",
        "car_reg": booking["car_reg_number"],
        "services": completed_services,
        "subtotal": subtotal,
        "gst_rate": int(gst_rate * 100),
        "gst_amount": gst_amount,
        "total": total
    }


def prepare_query_response_data(query_email: str, query_text: str, response_text: str) -> Dict[str, Any]:
    return {
        "query": query_text,
        "response": response_text,
        "response_date": datetime.now().strftime("%B %d, %Y %I:%M %p")
    }


# --------------------------------------------------------
# Main Notification Sender (Greenlet-safe)
# --------------------------------------------------------
async def send_notification(
    db: Session,
    notification_type: str,
    recipient_email: str,
    booking_id: Optional[int] = None,
    progress: Optional[BookingProgress] = None,
    query_data: Optional[Dict[str, str]] = None
):
    try:
        # Load booking if required
        booking_data = None
        if booking_id:
            booking = await fetch_booking_with_relations(db, booking_id)
            booking_data = serialize_booking(booking)

        # Determine email type
        if notification_type == NotificationType.BOOKING_CONFIRMATION:
            template_data = prepare_booking_confirmation_data(booking_data)
            subject = f"Booking Confirmed - #{booking_data['id']}"
            template_name = "booking_confirmation.html"
            category_name = "Booking Confirmation"

        elif notification_type == NotificationType.PROGRESS_UPDATE:
            if not progress:
                raise ValueError("Progress object required for progress update")
            template_data = prepare_progress_update_data(booking_data, progress)
            subject = f"Service Update - Booking #{booking_data['id']}"
            template_name = "progress_update.html"
            category_name = "Progress Update"

        elif notification_type == NotificationType.INVOICE:
            template_data = prepare_invoice_data(booking_data)
            subject = f"Invoice - Booking #{booking_data['id']}"
            template_name = "invoice.html"
            category_name = "Invoice"

        elif notification_type == NotificationType.QUERY_RESPONSE:
            if not query_data or not all(k in query_data for k in ['query', 'response']):
                raise ValueError("query_data with 'query' and 'response' is required")
            template_data = prepare_query_response_data(
                recipient_email,
                query_data['query'],
                query_data['response']
            )
            subject = "Response to Your Query"
            template_name = "query_response.html"
            category_name = "Query Response"

        else:
            raise ValueError(f"Invalid notification type: {notification_type}")

        # Send email
        message = MessageSchema(
            subject=subject,
            recipients=[recipient_email],
            template_body=template_data,
            subtype=MessageType.html
        )

        fm = FastMail(email_conf)
        await fm.send_message(message, template_name=template_name)

        # Log notification
        await log_notification(
            db=db,
            category_name=category_name,
            recipient_email=recipient_email,
            subject=subject
        )

        return {"status": "success", "message": f"Email sent to {recipient_email}"}

    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Failed to send email: {str(e)}")


# --------------------------------------------------------
# Convenience Wrappers
# --------------------------------------------------------
async def send_booking_confirmation(db: Session, booking_id: int):
    booking = await fetch_booking_with_relations(db, booking_id)
    return await send_notification(
        db=db,
        notification_type=NotificationType.BOOKING_CONFIRMATION,
        recipient_email=booking.customer.email,
        booking_id=booking_id
    )


async def send_progress_update(db: Session, booking_id: int, progress: BookingProgress):
    booking = await fetch_booking_with_relations(db, booking_id)
    return await send_notification(
        db=db,
        notification_type=NotificationType.PROGRESS_UPDATE,
        recipient_email=booking.customer.email,
        booking_id=booking_id,
        progress=progress
    )


async def send_invoice(db: Session, booking_id: int):
    booking = await fetch_booking_with_relations(db, booking_id)
    return await send_notification(
        db=db,
        notification_type=NotificationType.INVOICE,
        recipient_email=booking.customer.email,
        booking_id=booking_id
    )


async def send_query_response(db: Session, query_email: str, query_text: str, response_text: str):
    return await send_notification(
        db=db,
        notification_type=NotificationType.QUERY_RESPONSE,
        recipient_email=query_email,
        query_data={'query': query_text, 'response': response_text}
    )
