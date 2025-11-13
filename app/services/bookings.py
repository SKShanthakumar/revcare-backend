from fastapi import HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy import select, and_, desc, update, case
from sqlalchemy.ext.asyncio import AsyncSession as Session
from sqlalchemy.orm import selectinload
from sqlalchemy.exc import IntegrityError
from typing import Dict, Set, Optional, List
from datetime import datetime
from decimal import Decimal
import math

from app.models import (
    Booking, BookedService, BookingRecommendation, BookingAssignment, Car,
    BookingProgress, BookingAnalysis, Address, Status, CustomerCar, AssignmentType,
    Mechanic, PaymentMethod, OnlinePayment, OfflinePayment, ServiceSelectionStage,
    Service, Refund
)
from app.schemas import (
    BookingCreate, MechanicAssignmentCreate, BookingProgressCreate,
    BookingAnalysisCreate, CustomerServiceSelection, BookingProgressUpdate,
    BookingAnalysisUpdate, CashOnDelivery
)
from app.services import crud, payment as payment_service, notification as notification_service
from app.utilities.data_utils import get_gst_percent


# Helper Functions
async def get_status_id_by_name(db: Session, status_name: str) -> int:
    """
    Get status ID by status name.
    
    Args:
        db: Async database session
        status_name: Name of the status to look up
        
    Returns:
        int: Status ID
        
    Raises:
        HTTPException: 404 if status name is not found
    """
    result = await db.execute(select(Status).where(Status.name == status_name))
    status = result.scalar_one_or_none()
    if not status:
        raise HTTPException(status_code=404, detail=f"Status '{status_name}' not found")
    return status.id


async def get_or_create_address(db: Session, customer_id: str, address_id: Optional[int], address_data: Optional[Dict]) -> int:
    """
    Get existing address or create a new one.
    
    If address_id is provided, verifies it belongs to the customer and returns it.
    If address_data is provided, creates a new address and returns its ID.
    
    Args:
        db: Async database session
        customer_id: Customer ID to associate address with
        address_id: Optional existing address ID
        address_data: Optional dictionary with address data to create new address
        
    Returns:
        int: Address ID
        
    Raises:
        HTTPException: 
            - 404 if address_id is provided but not found or doesn't belong to customer
            - 400 if neither address_id nor address_data is provided
    """
    if address_id:
        # Verify address belongs to customer
        result = await db.execute(
            select(Address).where(
                and_(Address.id == address_id, Address.customer_id == customer_id)
            )
        )
        address = result.scalar_one_or_none()
        if not address:
            raise HTTPException(status_code=404, detail="Address not found or doesn't belong to customer")
        return address_id
    
    if address_data:
        # Create new address
        new_address = Address(customer_id=customer_id, **address_data)
        db.add(new_address)
        await db.flush()
        await db.refresh(new_address)
        return new_address.id
    
    raise HTTPException(status_code=400, detail="Either address_id or address data must be provided")


async def update_booking_status(db: Session, booking: Booking, status_name: str):
    """
    Update booking status and set completion time if delivered.
    
    Args:
        db: Async database session
        booking: Booking instance to update
        status_name: Name of the new status
        
    Raises:
        HTTPException: 400 if status name is invalid
    """
    status_id = await get_status_id_by_name(db, status_name)
    if not status_id:
        raise HTTPException(status_code=400, detail="Invalid booking status update.")
    booking.status_id = status_id
    if status_name == "delivered":
        booking.completed_at = datetime.now()
    await db.flush()


async def get_booking_progress_history(db: Session, booking: Booking):
    """
    Get validated booking progress history and analysis.
    
    Collects all validated progress updates and analysis reports for a booking
    and formats them into a chronological service history.
    
    Args:
        db: Async database session
        booking: Booking instance with loaded booking_progress and booking_analysis
        
    Returns:
        list: List of dictionaries containing status, description, images, mechanic, and timestamp
    """
    service_history = []
    for progress in booking.booking_progress:
        if progress.validated:
            service_history.append(
                {
                    "status": progress.status.name.lower(),
                    "description": progress.description,
                    "images": progress.images,
                    "mechanic": progress.mechanic.name,
                    "timestamp": progress.created_at
                }
            )
    
    analysis = booking.booking_analysis
    if analysis and analysis.validated:
        service_history.append(
            {
                "status": "analysis",
                "description": analysis.description,
                "images": analysis.images,
                "mechanic": analysis.mechanic.name,
                "timestamp": analysis.created_at
            }
        )

    return service_history


def get_latest_progress(booking_progress_list):
    """
    Get the most recent progress update from a list.
    
    Args:
        booking_progress_list: List of BookingProgress objects
        
    Returns:
        BookingProgress: The most recently created progress update
    """
    progress = sorted(booking_progress_list, key=lambda x: x.created_at, reverse=True)
    return progress[0] if progress else None

def get_latest_assignment(booking_assignment_list):
    """
    Get the most recent assignment from a list.
    
    Args:
        booking_assignment_list: List of BookingAssignment objects
        
    Returns:
        BookingAssignment: The most recently assigned booking assignment
    """
    assignment = sorted(booking_assignment_list, key=lambda x: x.assigned_at, reverse=True)
    return assignment[0] if assignment else None


async def cancelled_booking_returned(db: Session, booking_id: int):
    """
    Check if a cancelled booking has been returned (drop update exists).
    
    Args:
        db: Async database session
        booking_id: Booking ID to check
        
    Returns:
        bool: True if cancelled drop update exists, False otherwise
    """
    result = await db.execute(
        select(BookingProgress)
        .join(BookingProgress.status)
        .where(
            BookingProgress.booking_id == booking_id,
            Status.name == "cancelled"
        )
    )
    cancelled_drop_update = result.scalar_one_or_none()
    
    return cancelled_drop_update is not None


async def cancelled_drop_assigned(db: Session, booking_id: int):
    """
    Check if a cancelled booking has a drop assignment.
    
    Args:
        db: Async database session
        booking_id: Booking ID to check
        
    Returns:
        bool: True if cancelled drop assignment exists, False otherwise
    """
    result = await db.execute(
        select(BookingAssignment)
        .join(BookingAssignment.booking)
        .join(Status, Booking.status)
        .join(BookingAssignment.assignment_type)
        .where(
            BookingAssignment.booking_id == booking_id,
            Status.name == "cancelled",
            AssignmentType.name == "drop"
        )
    )
    assignment_obj = result.scalar_one_or_none()
    return assignment_obj is not None


def get_customer_status_mapping(booking: Booking):
    """
    Get condensed status mapping for customer view.
    
    Maps internal booking statuses to simplified customer-facing statuses.
    Used to provide a cleaner status representation for customers.
    
    Args:
        booking: Booking instance with booking_progress loaded
        
    Returns:
        dict: Mapping of internal status names to customer-facing status names
    """
    latest_update = get_latest_progress(booking.booking_progress)
    return {
        "booked": "booked",
        "pickup": "pickup",
        "received": "pickup",
        "analysis": "analysis",
        "analysed": "analysis",
        "in-progress": "in-progress",
        "completed": "completed",
        "out for delivery": "completed",
        "delivered": "delivered" if latest_update.validated else "completed",
        "cancelled": "cancelled"
    }


async def confirm_selected_services(db: Session, booking: Booking, selected_ids: Set[int], confirmed_status_id: int, rejected_status_id: int) -> None:
    """
    Confirm selected services and reject unselected services for a booking.
    
    Updates booked services status to 'confirmed' for selected services and
    'rejected' for services not in the selection. Also handles booking recommendations
    by creating new booked services for recommended services that were selected.
    
    Args:
        db: Async database session
        booking: Booking instance with booked_services and booking_recommendations loaded
        selected_ids: Set of service IDs that were selected by the customer
        confirmed_status_id: Status ID for confirmed services
        rejected_status_id: Status ID for rejected services
    """
    booked_services = {bs.service_id: bs for bs in booking.booked_services}
    recommendations = {br.service_id: br for br in booking.booking_recommendations}

    for service_id, bs in booked_services.items():
        bs.status_id = confirmed_status_id if service_id in selected_ids else rejected_status_id

    for service_id in selected_ids:
        if service_id in recommendations and service_id not in booked_services:
            rec = recommendations[service_id]
            db.add(BookedService(
                booking_id=booking.id,
                service_id=service_id,
                status_id=confirmed_status_id,
                est_price=rec.price,
                price=rec.price,
                completed=False
            ))


def check_all_booked_services_completed(booked_services: List[BookedService], confirmed_status_id: int):
    """
    Check if all booked services with confirmed status are marked as completed.
    
    Args:
        booked_services: List of BookedService instances
        confirmed_status_id: Status ID for confirmed services
        
    Returns:
        bool: True if all confirmed services are completed, False otherwise
    """
    completed = True
    for service in booked_services:
        if service.status_id == confirmed_status_id:
            completed = completed and service.completed
    return completed


async def add_cancellation_fee(db: Session, booking: Booking, cancellation_fee: float):
    """
    Add cancellation fee as an offline payment to a booking.
    
    Creates an offline payment record with pending status for the cancellation fee,
    including GST calculation, and associates it with the booking.
    
    Args:
        db: Async database session
        booking: Booking instance to add cancellation fee to
        cancellation_fee: Cancellation fee amount
        
    Returns:
        float: Total amount including GST
    """
    pending_status_id = await get_status_id_by_name(db, "pending")
    result = await db.execute(select(PaymentMethod).where(PaymentMethod.name.ilike("offline")))
    payment_method_obj = result.scalar_one_or_none()

    gst_rate = await get_gst_percent() * 0.01
    gst = cancellation_fee * gst_rate

    payment = OfflinePayment(
        booking_id = booking.id,
        status_id = pending_status_id,
        amount = cancellation_fee,
        gst = gst,
    )
    db.add(payment)

    booking.payment_method_id = payment_method_obj.id

    await db.flush()

    return cancellation_fee + gst


async def offline_payment_completed(db: Session, booking_id: int):
    """
    Check if any offline payment for a booking has been completed successfully.
    
    Args:
        db: Async database session
        booking_id: Booking ID to check payments for
        
    Returns:
        bool: True if at least one offline payment has status "success", False otherwise
    """
    result = await db.execute(select(OfflinePayment).where(OfflinePayment.booking_id == booking_id))
    booking_payments = result.scalars().all()
    for payment in booking_payments:
        if payment.status.name.lower() == "success":
            return True
    return False


async def get_online_payment_status(db: Session, booking_id: int):
    """
    Check if any online payment for a booking has been completed successfully.
    
    Args:
        db: Async database session
        booking_id: Booking ID to check payments for
        
    Returns:
        tuple: (bool, float) - (True if payment successful, amount_paid) or (False, -1)
    """
    result = await db.execute(select(OnlinePayment).where(OnlinePayment.booking_id == booking_id))
    booking_payments = result.scalars().all()
    for payment in booking_payments:
        if payment.status.name.lower() == "success":
            amount_paid = payment.amount + payment.gst
            return True, amount_paid
    return False, -1



# common functions
async def get_booking_by_id(db: Session, booking_id: int, payload: dict):
    """
    Get detailed booking information by ID with access control.
    
    Retrieves booking with all related entities (customer, car, addresses, progress, etc.)
    and calculates pricing including GST. Returns customer-friendly status for customers.
    
    Args:
        db: Async database session
        booking_id: Booking ID to retrieve
        payload: Token payload containing user_id and role
        
    Returns:
        dict: Detailed booking information with all related data
        
    Raises:
        HTTPException: 
            - 404 if booking is not found
            - 403 if customer tries to access another customer's booking
    """
    booking: Booking = await crud.get_one_record(
        db=db,
        model=Booking,
        filters={"id": booking_id},
        options=[
            selectinload(Booking.customer),
            selectinload(Booking.customer_car).selectinload(CustomerCar.car).selectinload(Car.manufacturer),
            selectinload(Booking.status),
            selectinload(Booking.pickup_address).selectinload(Address.area),
            selectinload(Booking.pickup_timeslot),
            selectinload(Booking.drop_address).selectinload(Address.area),
            selectinload(Booking.booking_progress).selectinload(BookingProgress.mechanic),
            selectinload(Booking.booking_progress).selectinload(BookingProgress.status),
            selectinload(Booking.booking_analysis).selectinload(BookingAnalysis.mechanic)
        ]
    )

    if not booking:
        raise HTTPException(status_code=404, detail="Booking not found.")

    if payload.get("role") == 3 and (booking.customer_id != payload.get("user_id")):
        raise HTTPException(status_code=403, detail="Operation not permitted. Trying to access data of other customers.")

    confirmed_status_id = await get_status_id_by_name(db, "confirmed")

    booked_services = [bs.service for bs in booking.booked_services if bs.status.name != "rejected"]
    total_est = sum(bs.est_price for bs in booking.booked_services)
    total_final = sum(bs.price for bs in booking.booked_services if bs.price and bs.status_id == confirmed_status_id) or None
    
    gst_rate = Decimal(str(await get_gst_percent() * 0.01)) # 18% GST
    if total_final is not None:
        gst_amount = total_final * gst_rate
        total_final += gst_amount

    gst_amount = total_est * gst_rate
    total_est += gst_amount

    booking_progress = await get_booking_progress_history(db, booking)

    response = {
        "id": booking.id,
        "status": get_customer_status_mapping(booking).get(booking.status.name.lower()) if payload.get("role") == 3 else booking.status.name,
        "customer": booking.customer,
        "car": {
            "manufacturer": booking.customer_car.car.manufacturer.name,
            "model": booking.customer_car.car.model,
            "reg_no": booking.car_reg_number,
            "img": booking.customer_car.car.img
        },
        "pickup": {
            "date": booking.pickup_date,
            "timeslot": booking.pickup_timeslot.name,
            "address": {
                "line1": booking.pickup_address.line1,
                "line2": booking.pickup_address.line2,
                "area": booking.pickup_address.area.name,
                "pincode": booking.pickup_address.area.pincode,
            }
        },
        "drop": {
            "date": booking.drop_date,
            "timeslot": booking.drop_timeslot.name,
            "address": {
                "line1": booking.drop_address.line1,
                "line2": booking.drop_address.line2,
                "area": booking.drop_address.area.name,
                "pincode": booking.drop_address.area.pincode,
            }
        },
        "booked_services": booked_services,
        "booking_progress": booking_progress,
        "total_estimated_price": float(total_est),
        "total_final_price": float(total_final) if total_final else None,
        "created_at": booking.created_at,
        "updated_at": booking.updated_at,
        "completed_at": booking.completed_at,
        "payment_method": booking.payment_method.name if booking.payment_method else None
    }

    return response


# Customer Functions
async def create_booking(db: Session, booking_data: BookingCreate, payload: dict):
    """
    Create a new booking for a customer.
    
    Validates customer ownership of car, calculates required service time,
    creates or uses existing addresses, and creates booking with booked services.
    Sends booking confirmation notification.
    
    Args:
        db: Async database session
        booking_data: Booking creation data including services, addresses, dates
        payload: Token payload containing user_id
        
    Returns:
        dict: Created booking information
        
    Raises:
        HTTPException: 
            - 403 if user is not a customer or doesn't own the car
            - 404 if service or car is not found
            - 403 if insufficient time between pickup and drop dates
            - 400 if there's invalid data or foreign key constraint
    """
    customer_id = payload.get("user_id")
    if not customer_id or not customer_id.startswith("CST"):
        raise HTTPException(status_code=403, detail="Only customers can create bookings.")
    
    # Verify customer owns the car
    car = await db.get(CustomerCar, booking_data.customer_car_id)
    if not car or car.customer_id != customer_id:
        raise HTTPException(status_code=403, detail="Car not found or doesn't belong to customer.")
    
    # drop date pickup date proper time gap check to complete all services
    hours_required = 0
    for service_id, _ in booking_data.service_price.items():
        service = await db.get(Service, service_id)
        if not service:
            raise HTTPException(status_code=404, detail="Service not found.")
        hours_required += service.time_hrs
    
    working_hours = 9
    days_required = math.ceil(hours_required / working_hours)
    customer_booked_days = (booking_data.drop_date - booking_data.pickup_date).days

    if customer_booked_days < days_required:
        raise HTTPException(status_code=403, detail=f"{days_required} day(s) are required to complete all the booked services.")

    
    # Get or create addresses
    pickup_address_id = await get_or_create_address(
        db, customer_id, booking_data.pickup_address_id, 
        booking_data.pickup_address.model_dump() if booking_data.pickup_address else None
    )
    drop_address_id = await get_or_create_address(
        db, customer_id, booking_data.drop_address_id,
        booking_data.drop_address.model_dump() if booking_data.drop_address else None
    )
    
    # Get 'booked' status
    booked_status_id = await get_status_id_by_name(db, "booked")
    
    # Create booking
    booking = Booking(
        customer_id=customer_id,
        car_reg_number=car.reg_number,
        status_id=booked_status_id,
        pickup_address_id=pickup_address_id,
        pickup_date=booking_data.pickup_date,
        pickup_timeslot_id=booking_data.pickup_timeslot_id,
        drop_address_id=drop_address_id,
        drop_date=booking_data.drop_date,
        drop_timeslot_id=booking_data.drop_timeslot_id
    )
    db.add(booking)
    
    try:
        await db.flush()
        await db.refresh(booking)
    except IntegrityError:
        import traceback
        traceback.print_exc()
        await db.rollback()
        raise HTTPException(status_code=400, detail="Invalid data or foreign key constraint")
    
    # Create booked services
    booked_services = []
    for service_id, est_price in booking_data.service_price.items():
        booked_services.append(BookedService(
            booking_id=booking.id,
            service_id=service_id,
            status_id=booked_status_id,
            est_price=est_price,
            price=None,
            completed=False
        ))
    db.add_all(booked_services)
    
    await db.commit()
    await db.refresh(booking)

    response = {
        "id": booking.id,
        "customer": booking.customer,
        "car": {
            "manufacturer": booking.customer_car.car.manufacturer.name,
            "model": booking.customer_car.car.model,
            "reg_no": booking.car_reg_number
        },
        "pickup": {
            "date": booking.pickup_date,
            "timeslot": booking.pickup_timeslot.name,
            "address": {
                "line1": booking.pickup_address.line1,
                "line2": booking.pickup_address.line2,
                "area": booking.pickup_address.area.name,
                "pincode": booking.pickup_address.area.pincode,
            }
        },
        "drop": {
            "date": booking.drop_date,
            "timeslot": booking.drop_timeslot.name,
            "address": {
                "line1": booking.drop_address.line1,
                "line2": booking.drop_address.line2,
                "area": booking.drop_address.area.name,
                "pincode": booking.drop_address.area.pincode,
            }
        },
        "created_at": booking.created_at
    }
    # await notification_service.send_booking_confirmation(db, booking.id)
    return response


async def get_customer_bookings(db: Session, payload: dict):
    """
    Get all bookings for a customer with simplified status mapping.
    
    Retrieves all bookings for the logged-in customer and formats them
    with customer-friendly status names and price quote validation status.
    
    Args:
        db: Async database session
        payload: Token payload containing user_id
        
    Returns:
        list: List of booking summaries with customer view format
        
    Raises:
        HTTPException: 403 if user is not a customer
    """
    customer_id = payload.get("user_id")
    if not customer_id or not customer_id.startswith("CST"):
        raise HTTPException(status_code=403, detail="Only customers can view their bookings")
    
    result = await db.execute(
        select(Booking)
        .options(
            selectinload(Booking.customer_car).selectinload(CustomerCar.car),
            selectinload(Booking.status),
        )
        .where(Booking.customer_id == customer_id)
        .order_by(desc(Booking.created_at))
    )
    bookings = result.scalars().all()
     
    customer_view = []
    for booking in bookings:
        validate_price_quote = booking.status.name == "analysed"
        if validate_price_quote:
            validate_price_quote = booking.booking_analysis.validated

        customer_view.append({
            "id": booking.id,
            "car": {
                "manufacturer": booking.customer_car.car.manufacturer.name,
                "model": booking.customer_car.car.model,
                "reg_no": booking.car_reg_number,
                "img": booking.customer_car.car.img
            },
            "status": get_customer_status_mapping(booking).get(booking.status.name.lower()),
            "validate_price": validate_price_quote,
            "pickup_date": booking.pickup_date,
            "drop_date": booking.drop_date,
            "created_at": booking.created_at
        })
    
    return customer_view


async def customer_confirm_services(db: Session, booking_id: int, selection: CustomerServiceSelection, payload: dict):
    """
    Customer confirms selected services after analysis and initiates payment.
    
    Validates booking status, calculates total price with GST, creates payment record
    (online or offline), and updates service selections. For online payments, creates
    Razorpay order and staging record.
    
    Args:
        db: Async database session
        booking_id: Booking ID to confirm services for
        selection: Customer service selection with service IDs and payment method
        payload: Token payload containing user_id
        
    Returns:
        JSONResponse: For online payments, returns Razorpay order details.
                     For offline payments, returns success message.
        
    Raises:
        HTTPException: 
            - 403 if booking doesn't belong to customer
            - 400 if booking is not in 'analysed' status
            - 400 if payment method is invalid
            - 500 if pending status is not found
    """
    customer_id = payload.get("user_id")
    
    # Verify booking belongs to customer
    booking = await db.get(Booking, booking_id)
    if not booking or booking.customer_id != customer_id:
        raise HTTPException(status_code=403, detail="Booking not found or access denied.")
    
    # Check if booking is in 'analysed' status
    valid_state = booking.status.name == "analysed"
    if valid_state:
        valid_state = booking.booking_analysis.validated

    if not valid_state:
        raise HTTPException(status_code=400, detail="Booking must be in 'analysed' status.")
    
    payment_method_obj = await db.get(PaymentMethod, selection.payment_method_id)
    if not payment_method_obj:
        raise HTTPException(status_code=400, detail="invalid payment method.")
    
    payment_method = payment_method_obj.name

    pending_status_id = await get_status_id_by_name(db, "pending")
    if not pending_status_id:
        raise HTTPException(status_code=500, detail="Pending status not found.")


    # validation over - based on payment type redirect to respective function
    # next step is to calculate amount to pay

    # Extract selected service prices
    booked_services = {bs.service_id: bs for bs in booking.booked_services}
    recommendations = {br.service_id: br for br in booking.booking_recommendations}

    selected_ids = set(selection.service_ids)
    total_price = 0

    for service_id in selected_ids:
        if service_id in booked_services:
            price = booked_services[service_id].price
        elif service_id in recommendations:
            price = recommendations[service_id].price
        else:
            price = 0    # discard - no need to raise error

        total_price += float(price)

    # Add GST
    gst_rate = await get_gst_percent() * 0.01
    gst_amount = total_price * gst_rate
    total_with_gst = total_price + gst_amount


    # separate online and offline payments
    if payment_method == "online":
        # create razorpay order
        razorpay_order = await payment_service.create_razorpay_order(total_with_gst)

        # add entry to db with payment in pending state
        payment = OnlinePayment(
            booking_id = booking.id,
            status_id = pending_status_id,
            amount = total_price,
            gst = gst_amount,
            razorpay_order_id = razorpay_order['id']
        )

        # staging table to get selected services when razorpay calls webhook to verify
        selection_stage = ServiceSelectionStage(
            booking_id = booking.id,
            razorpay_order_id = razorpay_order['id'],
            selected_services = selection.service_ids
        )

        db.add_all([payment, selection_stage])

        # update payment method
        booking.payment_method_id = selection.payment_method_id

        await db.commit()

        response = {
            "order_id": razorpay_order['id'],
            "amount": int(total_with_gst * 100)     # amount in paise
            }

        return JSONResponse(content=response)
    
    else:
        payment = OfflinePayment(
            booking_id = booking.id,
            status_id = pending_status_id,
            amount = total_price,
            gst = gst_amount,
        )
        db.add(payment)
    
        confirmed_status_id = await get_status_id_by_name(db, "confirmed")
        rejected_status_id = await get_status_id_by_name(db, "rejected")
        
        # confirm booked services
        await confirm_selected_services(db, booking, set(selection.service_ids), confirmed_status_id, rejected_status_id)
        
        # Update booking status to 'in-progress'
        booking.payment_method_id = selection.payment_method_id
        await update_booking_status(db, booking, "in-progress")
        
        await db.commit()
        
        return JSONResponse(content={"message": "Services confirmed successfully"})
    

async def cancel_booking(db: Session, booking_id: int, payload: dict):
    """
    Cancel a booking with cancellation fee calculation.
    
    Cancels a booking based on its current status. Calculates cancellation fees
    based on completed services for 'in-progress' bookings. Handles refunds for
    online payments. No fee for 'booked' or 'pickup' status bookings.
    
    Args:
        db: Async database session
        booking_id: Booking ID to cancel
        payload: Token payload containing user_id
        
    Returns:
        JSONResponse: Success message with cancellation fee
        
    Raises:
        HTTPException: 
            - 403 if booking doesn't belong to customer or is already cancelled
            - 403 if service is already completed
    """
    customer_id = payload.get("user_id")
    
    booking = await db.get(Booking, booking_id)
    if not booking or booking.customer_id != customer_id:
        raise HTTPException(status_code=403, detail="Booking not found or access denied.")
    

    current_booking_status = booking.status.name.lower()
    if current_booking_status == "cancelled":
        raise HTTPException(status_code=403, detail="Attempting invalid state transition.")

    if current_booking_status in ["completed", "out for delivery", "delivered"]:
        raise HTTPException(status_code=403, detail="Service is completed. Cancellation is not allowed.")
    
    elif current_booking_status in ["booked", "pickup"]:
        cancellation_fee_with_gst = 0    # No cancellation fee
    
    elif current_booking_status == "in-progress":
        confirmed_status_id = await get_status_id_by_name(db, "confirmed")
        total_amount = 0
        total_difficulty = 0
        for bs in booking.booked_services:
            service_difficulty = bs.service.difficulty
            if bs.status_id == confirmed_status_id and bs.completed:
                total_amount += bs.price * service_difficulty

            total_difficulty += service_difficulty

        cancellation_fee = float(total_amount) / max(total_difficulty, 1)
        if cancellation_fee < 100:
            cancellation_fee = 100

        gst_rate = await get_gst_percent() * 0.01
        gst = cancellation_fee * gst_rate
        cancellation_fee_with_gst = cancellation_fee + gst

        if booking.payment_method.name == "offline":
            result = await db.execute(select(OfflinePayment).where(OfflinePayment.booking_id == booking.id))
            payment_obj = result.scalar_one_or_none()

            payment_obj.amount = cancellation_fee
            payment_obj.gst = gst
            db.add(payment_obj)

        else:
            _, amount_paid = await get_online_payment_status(db, booking.id)
            refund_amount = max(float(amount_paid) - cancellation_fee_with_gst, 0)
            
            pending_state_id = await get_status_id_by_name(db, "pending")
            refund = Refund(
                booking_id = booking.id,
                customer_id = booking.customer_id,
                status_id = pending_state_id,
                amount = refund_amount
            )
            db.add(refund)
            cancellation_fee_with_gst = 0

    else:
        cancellation_fee = 100
        cancellation_fee_with_gst = await add_cancellation_fee(db, booking, cancellation_fee)

    await update_booking_status(db, booking, "cancelled")
    await db.commit()
    
    return JSONResponse(content={
        "message": "Booking cancelled successfully. Online payments will be refunded in 14 days.",
        "cancellation_fee": cancellation_fee
        })


# Admin Functions
async def get_admin_dashboard_bookings(db: Session, payload: dict, status_id: Optional[int] = None, action_required_filter: Optional[str] = None):
    """
    Get all bookings with action indicators for admin dashboard.
    
    Retrieves bookings with related data (customer, car, progress, analysis, assignments)
    and determines what actions are required (assign mechanic, validate progress, etc.).
    Can filter by status and action_required type.
    
    Args:
        db: Async database session
        payload: Token payload containing role
        status_id: Optional status ID to filter bookings
        action_required_filter: Optional filter for action type ("assign", "validate", "none")
        
    Returns:
        list: List of booking summaries with action indicators
        
    Raises:
        HTTPException: 403 if user is not an admin
    """
    user_role = payload.get("role")
    if user_role in [2, 3]:
        raise HTTPException(status_code=403, detail="Insufficient Permissions.")

    query = select(Booking).options(
        selectinload(Booking.customer),
        selectinload(Booking.customer_car).selectinload(CustomerCar.car).selectinload(Car.manufacturer),
        selectinload(Booking.status),
        selectinload(Booking.booking_progress).selectinload(BookingProgress.mechanic),
        selectinload(Booking.booking_analysis).selectinload(BookingAnalysis.mechanic),
        selectinload(Booking.booking_assignments).selectinload(BookingAssignment.mechanic)
    ).order_by(desc(Booking.created_at))
    
    if status_id is not None:
        query = query.where(Booking.status_id == status_id)
    
    result = await db.execute(query)
    bookings = result.scalars().all()
    
    dashboard_data = []
    for booking in bookings:
        status_name = booking.status.name.lower()
        action_required = "none"
        latest_progress = None
        latest_assignment = None
        analysis_report = None

        # fetch latest progress update
        if booking.booking_progress:
            latest_progress_obj = get_latest_progress(booking.booking_progress)
            latest_progress = {
                "id": latest_progress_obj.id,
                "description": latest_progress_obj.description,
                "mechanic": {
                    "id": latest_progress_obj.mechanic_id,
                    "name": latest_progress_obj.mechanic.name,
                },
                "validated": latest_progress_obj.validated,
                "timestamp": latest_progress_obj.created_at
            }

        # fetch booking assignment
        if booking.booking_assignments:
            sorted_assignments = sorted(booking.booking_assignments, key=lambda x: x.assigned_at, reverse=True)
            latest_assignment = {
                "id": sorted_assignments[0].id,
                "mechanic": {
                    "id": sorted_assignments[0].mechanic_id,
                    "name": sorted_assignments[0].mechanic.name,
                },
                "assignment_type": sorted_assignments[0].assignment_type.name,
                "status": sorted_assignments[0].status.name.lower()
            }

        # fetch analysis report
        if booking.booking_analysis:
            analysis_report = {
                "description": booking.booking_analysis.description,
                "recommendation": booking.booking_analysis.recommendation,
                "mechanic": {
                    "id": booking.booking_analysis.mechanic_id,
                    "name": booking.booking_analysis.mechanic.name,
                },
                "validated": booking.booking_analysis.validated
            }
        
        # Determine action required based on status
        if status_name in ["booked", "completed"]:
            action_required = "assign"
        
        elif status_name == "received":
            if latest_progress is not None:
                action_required = "assign" if latest_progress.get("validated") else "validate"
        
        elif status_name == "analysed":
            if analysis_report is not None:
                action_required = "waiting" if analysis_report.get("validated") else "validate"
        
        elif status_name == "in-progress":
            if latest_assignment and latest_assignment.get("status") == "completed":
                # Check latest progress
                if latest_progress:
                    if not latest_progress.get("validated"):
                        action_required = "validate"
                    else:
                        # Check if all services completed
                        booked_services_result = await db.execute(
                            select(BookedService).where(
                                and_(
                                    BookedService.booking_id == booking.id,
                                    BookedService.status_id == await get_status_id_by_name(db, "confirmed")
                                )
                            )
                        )
                        booked_services = booked_services_result.scalars().all()
                        all_completed = all(bs.completed for bs in booked_services)
                        action_required = "none" if all_completed else "assign"

        elif status_name == "delivered":
            if latest_progress is not None and not latest_progress.get("validated"):
                action_required = "validate"

        elif status_name == "cancelled" and booking.payment_method_id is not None:
            if not await cancelled_drop_assigned(db, booking.id):
                action_required = "assign"
            else:
                result = await db.execute(
                    select(BookingProgress)
                    .join(BookingProgress.status)
                    .where(
                        BookingProgress.booking_id == booking.id,
                        Status.name == "cancelled"
                    )
                )
                cancelled_drop_update = result.scalar_one_or_none() 
                if cancelled_drop_update and not cancelled_drop_update.validated:
                    action_required = "validate"

        # print(booking)
        dashboard_data.append({
            "booking_id": booking.id,
            "customer_name": booking.customer.name,
            "car_model": f"{booking.customer_car.car.manufacturer.name} {booking.customer_car.car.model}",
            "car_reg": booking.car_reg_number,
            "status": booking.status.name,
            "status_id": booking.status.id,
            "drop_date": booking.drop_date,
            "created_at": booking.created_at,
            "action_required": action_required,
            "latest_progress": latest_progress,
            "analysis_report": analysis_report,
            "latest_assignment": latest_assignment
        })
        
    if action_required_filter is not None:
        action_required_filter = action_required_filter.lower()
        dashboard_data = [data for data in dashboard_data if data.get("action_required") == action_required_filter]
    
    return dashboard_data


async def assign_mechanic(db: Session, assignment_data: MechanicAssignmentCreate):
    """
    Assign a mechanic to a booking for a specific assignment type.
    
    Validates booking status, mechanic qualifications, and assignment type.
    Updates booking status based on assignment type (pickup, analysis, drop, service).
    Sends notification to the assigned mechanic.
    
    Args:
        db: Async database session
        assignment_data: Assignment data with booking_id, mechanic_id, and assignment_type_id
        
    Returns:
        MechanicAssignmentResponse: Created assignment information
        
    Raises:
        HTTPException: 
            - 404 if booking, assignment type, or mechanic is not found
            - 400 if previous progress is not validated
            - 400 if mechanic is already assigned
            - 404 if mechanic is not qualified for the assignment type
            - 400 if invalid status transition
    """
    booking = await db.get(Booking, assignment_data.booking_id)
    if not booking:
        raise HTTPException(status_code=404, detail="Booking not found.")

    # fetch assignment type name
    assignment_type = await db.get(AssignmentType, assignment_data.assignment_type_id)
    current_booking_status = await db.get(Status, booking.status_id)

    if not assignment_type or not current_booking_status:
        raise HTTPException(status_code=404, detail="Assignment type not found or Booking is in invalid state.")
    
    # Check latest progress is validated before assigning
    if booking.booking_progress:
        latest_progress = get_latest_progress(booking.booking_progress)
        if not latest_progress.validated:
            raise HTTPException(status_code=400, detail="Validate and update previous progress to customer before assigning.")
    
    if booking.booking_assignments:
        latest_assignment = get_latest_assignment(booking.booking_assignments)
        if latest_assignment.status.name == "assigned":
            raise HTTPException(status_code=400, detail="Already assigned to a mechanic.")
        
    assignment_type_name = assignment_type.name.lower()

    # check mechanic qualification
    mechanic = await db.get(Mechanic, assignment_data.mechanic_id)
    if assignment_type_name == "analysis" and not mechanic.analysis:
        raise HTTPException(status_code=404, detail="Mechanic is not qualified for analysis.")
    if assignment_type_name in ["pickup", "drop"] and not mechanic.pickup_drop:
        raise HTTPException(status_code=404, detail="Mechanic is not qualified for pickup or drop.")
    
    # check valid status transition
    current_booking_status_name = current_booking_status.name.lower()
    
    if assignment_type_name == "pickup" and current_booking_status_name == 'booked':
        await update_booking_status(db, booking, "pickup")

    elif assignment_type_name == "analysis" and current_booking_status_name == 'received':
        await update_booking_status(db, booking, "analysis")
    
    elif assignment_type_name == "service" and current_booking_status_name == 'in-progress':
        pass

    elif assignment_type_name == "drop" and current_booking_status_name == 'completed':
        await update_booking_status(db, booking, "out for delivery")

    elif assignment_type_name == "drop" and current_booking_status_name == 'cancelled'and booking.payment_method_id is not None and not await cancelled_drop_assigned(db, booking.id):
        pass

    else:
        raise HTTPException(status_code=400, detail="Attempting invalid state transition")
    
    assigned_status_id = await get_status_id_by_name(db, "assigned")
    
    # Create assignment
    assignment = BookingAssignment(
        mechanic_id=assignment_data.mechanic_id,
        booking_id=assignment_data.booking_id,
        note=assignment_data.note,
        assignment_type_id=assignment_data.assignment_type_id,
        status_id=assigned_status_id
    )
    db.add(assignment)
    
    await db.commit()
    await db.refresh(assignment)
    
    return assignment


# Mechanic Functions
async def get_mechanic_assignments(db: Session, payload: dict):
    """
    Get all assignments for the logged-in mechanic.
    
    Retrieves all booking assignments for the mechanic, excluding assignments
    for cancelled bookings (except drop assignments for cancelled bookings).
    
    Args:
        db: Async database session
        payload: Token payload containing user_id
        
    Returns:
        list: List of assignment information with booking details
        
    Raises:
        HTTPException: 403 if user is not a mechanic or admin
    """
    mechanic_id = payload.get("user_id")
    if not mechanic_id or mechanic_id.startswith("CST"):
        raise HTTPException(status_code=403, detail="Only mechanics or admin can view assignments")
    
    result = await db.execute(
        select(BookingAssignment)
        .options(
            selectinload(BookingAssignment.booking),
            selectinload(BookingAssignment.assignment_type),
            selectinload(BookingAssignment.status)
        )
        .where(BookingAssignment.mechanic_id == mechanic_id)
        .order_by(desc(BookingAssignment.assigned_at))
    )

    assignments = result.scalars().all()
    result = []
    for assignment in assignments:
        # If booking is cancelled - if assignment type is drop then it is for returning the car so it can be sent
        if assignment.booking.status.name.lower() == "cancelled" and assignment.assignment_type.name != "drop":
            continue    # need not show assignment of cancelled bookings

        # Otherwise include it in the output
        result.append(
            {
                "id": assignment.id,
                "assignment_type": assignment.assignment_type.name,
                "status": assignment.status.name,
                "note": assignment.note,
                "booking_id": assignment.booking_id,
                "assigned_at": assignment.assigned_at
            }
        )

    return result


async def create_progress_update(db: Session, progress_data: BookingProgressCreate, payload: dict):
    """
    Create a progress update for a booking.
    
    Allows mechanics to update booking progress (pickup, received, out for delivery, delivered, cancelled).
    Marks services as completed for 'in-progress' status. Updates booking status and assignment status.
    Validates payment for offline payments before delivery.
    
    Args:
        db: Async database session
        progress_data: Progress update data with description, images, and service IDs
        payload: Token payload containing user_id
        
    Returns:
        BookingProgress: Created progress update
        
    Raises:
        HTTPException: 
            - 403 if user is not a mechanic or doesn't own the assignment
            - 404 if booking is not found or progress already exists
            - 400 if invalid status transition or payment not completed for offline payments
    """
    mechanic_id = payload.get("user_id")
    if not mechanic_id or not mechanic_id.startswith("MEC"):
        raise HTTPException(status_code=403, detail="Only mechanics can create progress updates.")
    
    booking = await db.get(Booking, progress_data.booking_id)
    if not booking:
        raise HTTPException(status_code=404, detail="Booking not found.")
    
    if booking.booking_assignments:
        sorted_assignments = sorted(booking.booking_assignments, key=lambda x: x.assigned_at, reverse=True)
        if sorted_assignments[0].mechanic_id != mechanic_id:
            raise HTTPException(status_code=403, detail="Trying to access other mechanic assignments.")
    
    # Check latest progress is validated before assigning
    if booking.booking_progress:
        latest_progress = get_latest_progress(booking.booking_progress)
        if not latest_progress.validated:
            raise HTTPException(status_code=404, detail="Already updated progress.")
    
    current_booking_status = booking.status.name.lower()
    valid_states = ["pickup", "in-progress", "out for delivery", "cancelled"]

    if current_booking_status not in valid_states:
        raise HTTPException(status_code=400, detail="Attempting invalid state transition.")
    

    # Mark services as completed
    if current_booking_status == "in-progress" and progress_data.services_completed_ids is not None:
        await db.execute(
            update(BookedService)
            .where(
                BookedService.booking_id == progress_data.booking_id,
                BookedService.service_id.in_(progress_data.services_completed_ids),
            )
            .values(completed=True)
        )

    # offline payment check
    elif current_booking_status == "out for delivery" and booking.payment_method.name == "offline" and not await offline_payment_completed(db, booking.id):
        raise HTTPException(status_code=400, detail="Payment not yet made. Collect cash from customer.")

    elif current_booking_status == "cancelled":
        if booking.payment_method_id is None or await cancelled_booking_returned(db, booking.id):
            raise HTTPException(status_code=400, detail="Attempting invalid state transition.")

        if booking.payment_method.name == "offline" and not await offline_payment_completed(db, booking.id):
            raise HTTPException(status_code=400, detail="Payment not yet made. Collect cash from customer.")
        
    # Create progress update
    progress = BookingProgress(
        mechanic_id=mechanic_id,
        booking_id=progress_data.booking_id,
        description=progress_data.description,
        images=progress_data.images,
        status_id=booking.status_id,
        completed_service_ids=progress_data.services_completed_ids,
        validated=False
    )
    db.add(progress)

    # Update booking status based on current status
    if current_booking_status == "pickup":
        await update_booking_status(db, booking, "received")
    elif current_booking_status == "out for delivery":
        await update_booking_status(db, booking, "delivered")
    
    # Update assignment status to completed
    result = await db.execute(
        select(BookingAssignment)
        .where(
            and_(
                BookingAssignment.booking_id == progress_data.booking_id,
                BookingAssignment.mechanic_id == mechanic_id
            )
        )
        .order_by(desc(BookingAssignment.assigned_at))
    )
    latest_assignment = result.scalars().first()
    if latest_assignment:
        completed_status_id = await get_status_id_by_name(db, "completed")
        latest_assignment.status_id = completed_status_id
    
    await db.commit()
    await db.refresh(progress)
    
    return progress


async def create_analysis(db: Session, analysis_data: BookingAnalysisCreate, payload: dict):
    """
    Create an analysis report for a booking.
    
    Allows mechanics to create analysis reports with price quotes for all booked services
    and recommended services. Updates booked service prices and creates recommendations.
    Updates booking status to 'analysed'.
    
    Args:
        db: Async database session
        analysis_data: Analysis data with description, recommendation, price quotes, and recommended services
        payload: Token payload containing user_id
        
    Returns:
        BookingAnalysis: Created analysis report
        
    Raises:
        HTTPException: 
            - 403 if user is not a mechanic or doesn't own the assignment
            - 404 if booking is not found
            - 400 if booking is not in 'analysis' status
            - 400 if price quotes are not provided for all booked services
    """
    mechanic_id = payload.get("user_id")
    if not mechanic_id or not mechanic_id.startswith("MEC"):
        raise HTTPException(status_code=403, detail="Only mechanics can create analysis")
    
    booking = await db.get(Booking, analysis_data.booking_id)
    if not booking:
        raise HTTPException(status_code=404, detail="Booking not found")
    
    if booking.booking_assignments:
        sorted_assignments = sorted(booking.booking_assignments, key=lambda x: x.assigned_at, reverse=True)
        if sorted_assignments[0].mechanic_id != mechanic_id:
            raise HTTPException(status_code=403, detail="Trying to access other mechanic assignments.")
    
    current_booking_status = booking.status.name.lower()
    if current_booking_status != "analysis":
        raise HTTPException(status_code=400, detail="Attempting invalid state transition")
    
    # check price quote given for all booked services
    given_service_ids = set(analysis_data.price_quote.keys())

    booked_service_ids = { service.service_id for service in booking.booked_services }
    if len(booked_service_ids - given_service_ids) != 0:
        raise HTTPException(status_code=400, detail="Provide price-quote for all booked services.")
    
    # Create analysis
    analysis = BookingAnalysis(
        booking_id=analysis_data.booking_id,
        mechanic_id=mechanic_id,
        description=analysis_data.description,
        recommendation=analysis_data.recommendation,
        images=analysis_data.images,
        validated=False
    )
    db.add(analysis)
    
    # Update booked services prices
    if len(analysis_data.price_quote) <= 5:
        # Small updates -> simpler loop
        for service_id, price in analysis_data.price_quote.items():
            await db.execute(
                update(BookedService)
                .where(
                    BookedService.booking_id == analysis_data.booking_id,
                    BookedService.service_id == service_id,
                )
                .values(price=price)
            )
    else:
        # Large updates -> one query with CASE
        price_cases = case(
            {
                service_id: price for service_id, price in analysis_data.price_quote.items()
            },
            value=BookedService.service_id,
        )

        await db.execute(
            update(BookedService)
            .where(
                BookedService.booking_id == analysis_data.booking_id,
                BookedService.service_id.in_(analysis_data.price_quote.keys()),
            )
            .values(price=price_cases)
        )


    # add recommended services to db
    if analysis_data.recommended_services:

        recommendations = [
            BookingRecommendation(
                booking_id=analysis_data.booking_id,
                service_id=service_id,
                price=price
            )
            for service_id, price in analysis_data.recommended_services.items()
            if service_id not in booked_service_ids
        ]
        db.add_all(recommendations)
    
    # Update booking status to 'analysed'
    await update_booking_status(db, booking, "analysed")
    
    # Update assignment to completed
    result = await db.execute(
        select(BookingAssignment)
        .where(
            and_(
                BookingAssignment.booking_id == analysis_data.booking_id,
                BookingAssignment.mechanic_id == mechanic_id
            )
        )
        .order_by(desc(BookingAssignment.assigned_at))
    )
    latest_assignment = result.scalars().first()
    if latest_assignment:
        completed_status_id = await get_status_id_by_name(db, "completed")
        latest_assignment.status_id = completed_status_id
    
    await db.commit()
    await db.refresh(analysis)
    
    return analysis


async def receive_cash_on_delivery(db: Session, booking_id: int, request_body: CashOnDelivery, payload: dict):
    """
    Receive cash on delivery payment for a booking.
    
    Allows mechanics assigned to drop assignment to receive payment for offline payments.
    Can process offline payment directly or create online payment order if customer wants to pay online.
    Sends invoice notification after successful offline payment.
    
    Args:
        db: Async database session
        booking_id: Booking ID to receive payment for
        request_body: Cash on delivery data with payment method
        payload: Token payload containing user_id
        
    Returns:
        JSONResponse: For online payments, returns Razorpay order details.
                     For offline payments, returns success message.
        
    Raises:
        HTTPException: 
            - 403 if mechanic is not assigned to drop or payment already completed
            - 400 if booking is not in valid status or payment method is invalid
    """
    mechanic_id = payload.get("user_id")
    
    # Verify booking belongs to customer
    result = await db.execute(
        select(BookingAssignment)
        .join(BookingAssignment.assignment_type)
        .where(
            BookingAssignment.booking_id == booking_id,
            AssignmentType.name == "drop",
            BookingAssignment.mechanic_id == mechanic_id
        )
        .options(selectinload(BookingAssignment.booking))
    )

    assignment = result.scalar_one_or_none()    
    if not assignment:
        raise HTTPException(status_code=403, detail="Access denied.")
    
    booking = assignment.booking
    if not booking:
        raise HTTPException(status_code=403, detail="Booking not found.")

    # Check if booking is in 'analysed' status
    valid_state = (booking.status.name == "out for delivery" or booking.status.name == "cancelled") and booking.payment_method.name == "offline"
    if not valid_state:
        raise HTTPException(status_code=400, detail="Booking must be in 'out for delivery' or 'cancelled' status and also opted for cash on delivery.")
    
    if await offline_payment_completed(db, booking.id):
        raise HTTPException(status_code=403, detail="Payment already completed.")
    
    payment_method_obj = await db.get(PaymentMethod, request_body.payment_method_id)
    if not payment_method_obj:
        raise HTTPException(status_code=400, detail="invalid payment method.")
    

    # next step is to calculate amount to pay
    result = await db.execute(select(OfflinePayment).where(OfflinePayment.booking_id == booking.id))
    payment_obj = result.scalar_one_or_none()

    total_price = payment_obj.amount

    # Add GST
    gst_amount = payment_obj.gst
    total_with_gst = total_price + gst_amount

    payment_method = payment_method_obj.name

    # separate online and offline payments
    if payment_method == "online":
        # create razorpay order
        razorpay_order = await payment_service.create_razorpay_order(total_with_gst)
        pending_status_id = await get_status_id_by_name(db, "pending")

        # add entry to db with payment in pending state
        payment = OnlinePayment(
            booking_id = booking.id,
            status_id = pending_status_id,
            amount = total_price,
            gst = gst_amount,
            razorpay_order_id = razorpay_order['id']
        )

        db.add(payment)

        await db.commit()

        response = {
            "order_id": razorpay_order['id'],
            "amount": int(total_with_gst * 100)     # amount in paise
            }

        return JSONResponse(content=response)
    
    else:
        payment_obj.status_id = await get_status_id_by_name(db, "success")
        
        await db.commit()
        # await notification_service.send_invoice(db, booking.id)
        
        return JSONResponse(content={"message": "Payment received successfully"})


# Admin validation functions
async def update_progress(db: Session, progress_id: int, update_data: BookingProgressUpdate):
    """
    Update a progress record (admin edit).
    
    Allows admin to edit progress update details before validation.
    Cannot update progress that has already been validated.
    
    Args:
        db: Async database session
        progress_id: Progress record ID to update
        update_data: Updated progress data
        
    Returns:
        BookingProgress: Updated progress record
        
    Raises:
        HTTPException: 
            - 404 if progress record is not found
            - 400 if progress is already validated
    """
    result = await db.execute(
        select(BookingProgress)
        .options(selectinload(BookingProgress.booking))
        .where(BookingProgress.id == progress_id)
    )
    progress = result.scalar_one_or_none()
    if not progress:
        raise HTTPException(status_code=404, detail="Progress record not found")
    
    if progress.validated:
        raise HTTPException(status_code=400, detail="Progress already validated.")
    
    update_dict = update_data.model_dump(exclude_none=True)
    for key, value in update_dict.items():
        if hasattr(progress, key):  # avoid attribute errors
            setattr(progress, key, value)

    # if admin tries to change the completed services
    if progress.status_id == await get_status_id_by_name(db, "in-progress"):
        if update_data.completed_service_ids is not None:
            completed_ids = set(update_data.completed_service_ids)
            for bs in progress.booking.booked_services:
                bs.completed = bs.service_id in completed_ids
    
    await db.commit()
    await db.refresh(progress)
    
    return progress


async def validate_progress(db: Session, progress_id: int):
    """
    Validate and approve a progress update.
    
    Validates progress update, awards score to mechanic based on completed services,
    updates booking status to 'completed' if all services are done, and sends
    progress update notification to customer.
    
    Args:
        db: Async database session
        progress_id: Progress record ID to validate
        
    Returns:
        JSONResponse: Success message
        
    Raises:
        HTTPException: 
            - 404 if progress record is not found
            - 400 if progress is already validated
    """
    result = await db.execute(
        select(BookingProgress)
        .options(selectinload(BookingProgress.booking))
        .where(BookingProgress.id == progress_id)
    )
    progress = result.scalar_one_or_none()
    if not progress:
        raise HTTPException(status_code=404, detail="Progress record not found.")
    
    if progress.validated:
        raise HTTPException(status_code=400, detail="Progress already validated.")
    
    mechanic = await db.get(Mechanic, progress.mechanic_id)
  
    if progress.status_id == await get_status_id_by_name(db, "in-progress"):
        # add score to mechanic
        booked_services = progress.booking.booked_services
        service_completed_by_mechanic = progress.completed_service_ids

        if service_completed_by_mechanic:
            score = 0
            for bs in booked_services:
                if bs.completed and bs.service_id in service_completed_by_mechanic:
                    score += bs.service.difficulty

            if mechanic:
                mechanic.score = (mechanic.score or 0) + score

        # if all services are completed, change booking to completed state
        confirmed_status_id = await get_status_id_by_name(db, "confirmed")
        if check_all_booked_services_completed(booked_services, confirmed_status_id):
            await update_booking_status(db, progress.booking, "completed")
    
    elif mechanic:
        mechanic.score = (mechanic.score or 0) + 2  # difficulty 2 for pickup and drop

    progress.validated = True
    # await notification_service.send_progress_update(db, progress.booking_id, progress)
    
    await db.commit()
    
    return JSONResponse(content={"message": "Progress validated and sent to customer"})


async def update_analysis(db: Session, booking_id: int, update_data: BookingAnalysisUpdate):
    """
    Update an analysis report (admin edit).
    
    Allows admin to edit analysis report details before validation.
    Cannot update analysis that has already been validated.
    
    Args:
        db: Async database session
        booking_id: Booking ID (used as analysis primary key)
        update_data: Updated analysis data
        
    Returns:
        BookingAnalysis: Updated analysis record
        
    Raises:
        HTTPException: 
            - 404 if analysis record is not found
            - 400 if analysis is already validated
    """
    analysis = await db.get(BookingAnalysis, booking_id)
    if not analysis:
        raise HTTPException(status_code=404, detail="Analysis record not found")
    
    if analysis.validated:
        raise HTTPException(status_code=400, detail="Analysis already validated.")
    
    update_dict = update_data.model_dump(exclude_none=True)
    for key, value in update_dict.items():
        setattr(analysis, key, value)
    
    await db.commit()
    await db.refresh(analysis)
    
    return analysis


async def validate_analysis(db: Session, booking_id: int):
    """
    Validate and approve an analysis report.
    
    Validates analysis report, awards score to mechanic (difficulty 3 for analysis),
    and marks analysis as validated so it can be sent to customer.
    
    Args:
        db: Async database session
        booking_id: Booking ID (used as analysis primary key)
        
    Returns:
        JSONResponse: Success message
        
    Raises:
        HTTPException: 
            - 404 if analysis record is not found
            - 400 if analysis is already validated
    """
    analysis = await db.get(BookingAnalysis, booking_id)
    if not analysis:
        raise HTTPException(status_code=404, detail="Analysis record not found")
    
    if analysis.validated:
        raise HTTPException(status_code=400, detail="Analysis already validated.")
    
    mechanic = await db.get(Mechanic, analysis.mechanic_id)
    if mechanic:
        mechanic.score = (mechanic.score or 0) + 3  # difficulty 3 analysis
    
    analysis.validated = True
    
    await db.commit()
    
    return JSONResponse(content={"message": "Analysis validated and sent to customer"})


async def confirm_booking_webhook(db: Session, order_id: str, payment_id: str, signature: str):
    """
    Webhook handler for confirming payment and booking service selection.
    
    Verifies Razorpay payment signature, updates payment status, confirms selected services
    from staging table, updates booking status to 'in-progress', and sends invoice notification.
    Used when customer pays online after service selection.
    
    Args:
        db: Async database session
        order_id: Razorpay order ID
        payment_id: Razorpay payment ID
        signature: Razorpay payment signature for verification
        ~
    Returns:
        JSONResponse: Success message
        
    Raises:
        HTTPException: 
            - 404 if payment record or order staging is not found
            - 400 if payment signature is invalidorder
            - 500 if payment verification fails
    """
    # fetch payment object
    result = await db.execute(
        select(OnlinePayment).where(OnlinePayment.razorpay_order_id == order_id)
    )
    payment = result.scalar_one_or_none()
    if not payment:
        raise HTTPException(status_code=404, detail="Payment record not found.")

    success_status_id = await get_status_id_by_name(db, "success")
    if payment.status_id == success_status_id:
        return JSONResponse(content={"message": "Payment already verified."})
    
    try:
        if not payment_service.verify_signature(order_id, payment_id, signature):
            payment.razorpay_payment_id = payment_id
            payment.razorpay_signature = signature
            payment.status_id = await get_status_id_by_name(db, "failed")
            await db.commit()
            raise HTTPException(status_code=400, detail="Invalid payment signature")
    except Exception as e:
        payment.status_id = await get_status_id_by_name(db, "failed")
        await db.commit()
        raise HTTPException(status_code=500, detail=f"Payment verification error: {str(e)}")

    
    # update payment success
    payment.razorpay_payment_id = payment_id
    payment.razorpay_signature = signature
    payment.status_id = success_status_id

    
    # fetch selection from stage
    result = await db.execute(
        select(ServiceSelectionStage).where(ServiceSelectionStage.razorpay_order_id == order_id)
    )
    selection = result.scalar_one_or_none()
    if not selection:
        raise HTTPException(status_code=404, detail="Order not found in staging table.")

    booking = await db.get(Booking, selection.booking_id)
    if not booking:
        raise HTTPException(status_code=403, detail="Booking not found.")
    

    # confirm booked servies
    confirmed_status_id = await get_status_id_by_name(db, "confirmed")
    rejected_status_id = await get_status_id_by_name(db, "rejected")

    # confirm booked services
    await confirm_selected_services(db, booking, set(selection.selected_services), confirmed_status_id, rejected_status_id)
    
    # Update booking status to 'in-progress'
    await update_booking_status(db, booking, "in-progress")
       
    await db.commit()
    # await notification_service.send_invoice(db, booking.id)
    
    return JSONResponse(content={"message": "Payment successful."})

async def confirm_payment_webhook(db: Session, order_id: str, payment_id: str, signature: str):
    """
    Webhook handler for confirming cash on delivery payment.
    
    Verifies Razorpay payment signature for COD orders, updates online payment status,
    marks offline payment as paid online, and sends invoice notification.
    Used when customer pays online at the time of delivery instead of cash.
    
    Args:
        db: Async database session
        order_id: Razorpay order ID
        payment_id: Razorpay payment ID
        signature: Razorpay payment signature for verification
        
    Returns:
        JSONResponse: Success message
        
    Raises:
        HTTPException: 
            - 404 if payment record is not found
            - 400 if payment signature is invalid
            - 500 if payment verification fails
    """
    # fetch payment object
    result = await db.execute(
        select(OnlinePayment).where(OnlinePayment.razorpay_order_id == order_id)
    )
    payment = result.scalar_one_or_none()
    if not payment:
        raise HTTPException(status_code=404, detail="Payment record not found.")

    success_status_id = await get_status_id_by_name(db, "success")
    if payment.status_id == success_status_id:
        return JSONResponse(content={"message": "Payment already verified."})
    
    try:
        if not payment_service.verify_signature(order_id, payment_id, signature):
            payment.razorpay_payment_id = payment_id
            payment.razorpay_signature = signature
            payment.status_id = await get_status_id_by_name(db, "failed")
            await db.commit()
            raise HTTPException(status_code=400, detail="Invalid payment signature")
    except Exception as e:
        payment.status_id = await get_status_id_by_name(db, "failed")
        await db.commit()
        raise HTTPException(status_code=500, detail=f"Payment verification error: {str(e)}")

    
    # update payment success
    payment.razorpay_payment_id = payment_id
    payment.razorpay_signature = signature
    payment.status_id = success_status_id

    
    # update offline payment entry
    result = await db.execute(select(OfflinePayment).where(OfflinePayment.booking_id == payment.booking_id))
    payment_obj = result.scalar_one_or_none()

    payment_obj.status_id = success_status_id
    payment_obj.paid_online = True
    
    await db.commit()
    # await notification_service.send_invoice(db, payment_obj.booking_id)
    
    return JSONResponse(content={"message": "Payment received successfully"})
