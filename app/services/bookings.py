from fastapi import HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy import select, and_, desc, update, case
from sqlalchemy.ext.asyncio import AsyncSession as Session
from sqlalchemy.orm import selectinload
from sqlalchemy.exc import IntegrityError
from typing import Dict, Set, Optional, List
from datetime import datetime

from app.models import (
    Booking, BookedService, BookingRecommendation, BookingAssignment, Car,
    BookingProgress, BookingAnalysis, Address, Status, CustomerCar, AssignmentType,
    Mechanic, PaymentMethod, OnlinePayment, OfflinePayment, ServiceSelectionStage
)
from app.schemas import (
    BookingCreate, MechanicAssignmentCreate, BookingProgressCreate,
    BookingAnalysisCreate, CustomerServiceSelection, BookingProgressUpdate,
    BookingAnalysisUpdate
)
from app.services import crud, payment as payment_service


# condensed status for customer view
customer_status_mapping = {
    "booked": "booked",
    "pickup": "pickup",
    "received": "pickup",
    "analysis": "analysis",
    "analysed": "analysis",
    "in-progress": "in-progress",
    "completed": "completed",
    "out for delivery": "completed",
    "delivered": "delivered",
    "cancelled": "cancelled"
}

# Helper Functions
async def get_status_id_by_name(db: Session, status_name: str) -> int:
    """Get status ID by status name"""
    result = await db.execute(select(Status).where(Status.name == status_name))
    status = result.scalar_one_or_none()
    if not status:
        raise HTTPException(status_code=404, detail=f"Status '{status_name}' not found")
    return status.id


async def get_or_create_address(db: Session, customer_id: str, address_id: Optional[int], address_data: Optional[Dict]) -> int:
    """Get existing address or create new one"""
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
    """Update booking status"""
    status_id = await get_status_id_by_name(db, status_name)
    if not status_id:
        raise HTTPException(status_code=400, detail="Invalid booking status update.")
    booking.status_id = status_id
    if status_name == "delivered":
        booking.completed_at = datetime.now()
    await db.flush()


async def get_booking_progress_history(db: Session, booking: Booking):
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
    return sorted(booking_progress_list, key=lambda x: x.created_at, reverse=True)[0]


async def confirm_selected_services(db: Session, booking: Booking, selected_ids: Set[int], confirmed_status_id: int, rejected_status_id: int) -> None:
    """
    Update booking services based on customer selection.
    Confirms selected services and rejects the rest.

    Args:
        db (AsyncSession): SQLAlchemy async database session
        booking (Booking): Booking object containing booked and recommended services
        selected_ids (Set[int]): IDs of services selected by the customer
        confirmed_status_id (int): Status ID for confirmed services
        rejected_status_id (int): Status ID for rejected services

    Returns:
        None
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
    completed = True
    for service in booked_services:
        if service.status_id == confirmed_status_id:
            completed = completed and service.completed
    return completed

# common functions
async def get_booking_by_id(db: Session, booking_id: int, payload: dict):
    """Get detailed booking by ID"""
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

    booked_services = [bs.service for bs in booking.booked_services]
    total_est = sum(bs.est_price for bs in booking.booked_services)
    total_final = sum(bs.price for bs in booking.booked_services if bs.price and bs.status_id == confirmed_status_id) or None
    booking_progress = await get_booking_progress_history(db, booking)

    response = {
        "id": booking.id,
        "status": customer_status_mapping.get(booking.status.name.lower()) if payload.get("role") == 3 else booking.status.name,
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
    """Customer creates a new booking"""
    customer_id = payload.get("user_id")
    if not customer_id or not customer_id.startswith("CST"):
        raise HTTPException(status_code=403, detail="Only customers can create bookings")
    
    # Verify customer owns the car
    car = await db.get(CustomerCar, booking_data.customer_car_id)
    if not car or car.customer_id != customer_id:
        raise HTTPException(status_code=403, detail="Car not found or doesn't belong to customer")
    
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
    for service_id, est_price in booking_data.service_price.items():
        booked_service = BookedService(
            booking_id=booking.id,
            service_id=service_id,
            status_id=booked_status_id,
            est_price=est_price,
            price=None,
            completed=False
        )
        db.add(booked_service)
    
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

    return response


async def get_customer_bookings(db: Session, payload: dict):
    """Get all bookings for a customer with grouped status"""
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
            "status": customer_status_mapping.get(booking.status.name.lower(), booking.status.name),
            "validate_price": validate_price_quote,
            "pickup_date": booking.pickup_date,
            "drop_date": booking.drop_date,
            "created_at": booking.created_at
        })
    
    return customer_view


async def customer_confirm_services(db: Session, booking_id: int, selection: CustomerServiceSelection, payload: dict):
    """Customer confirms services after analysis"""
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
    gst_rate = 0.18  # 18% GST
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

        return JSONResponse(content={"order_id": razorpay_order['id'], "amount": total_with_gst})
    
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
    """Customer cancels a booking"""
    customer_id = payload.get("user_id")
    
    booking = await db.get(Booking, booking_id)
    if not booking or booking.customer_id != customer_id:
        raise HTTPException(status_code=403, detail="Booking not found or access denied")
    
    await update_booking_status(db, booking, "cancelled")
    await db.commit()
    
    return JSONResponse(content={"message": "Booking cancelled successfully"})


# Admin Functions
async def get_admin_dashboard_bookings(db: Session, payload: dict, status_id: Optional[int] = None, action_required_filter: Optional[str] = None):
    """Get all bookings with action indicators for admin"""
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
        else:
            sorted_progress = None

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
        else:
            sorted_assignments = None

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


async def get_booked_services(db: Session, booking_id: int):
    """Get all services for a booking"""
    result = await db.execute(
        select(BookedService)
        .options(selectinload(BookedService.service), selectinload(BookedService.status))
        .where(BookedService.booking_id == booking_id)
    )
    return result.scalars().all()


async def assign_mechanic(db: Session, assignment_data: MechanicAssignmentCreate):
    """Admin assigns mechanic to a booking"""
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
            raise HTTPException(status_code=404, detail="Validate and update previous progress to customer before assigning.")
        
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

    else:
        raise HTTPException(status_code=400, detail="Attempting invalid state transition")
    
    assigned_status_id = await get_status_id_by_name(db, "assigned")
    
    # Create assignment
    assignment = BookingAssignment(
        mechanic_id=assignment_data.mechanic_id,
        booking_id=assignment_data.booking_id,
        assignment_type_id=assignment_data.assignment_type_id,
        status_id=assigned_status_id
    )
    db.add(assignment)
    
    await db.commit()
    await db.refresh(assignment)
    
    return assignment


# Mechanic Functions
async def get_mechanic_assignments(db: Session, payload: dict):
    """Get all assignments for a mechanic"""
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
        result.append(
            {
                "id": assignment.id,
                "assignment_type": assignment.assignment_type.name,
                "status": assignment.status.name,
                "booking_id": assignment.booking_id,
                "assigned_at": assignment.assigned_at
            }
        )

    return result


async def create_progress_update(db: Session, progress_data: BookingProgressCreate, payload: dict):
    """Mechanic creates progress update"""
    mechanic_id = payload.get("user_id")
    if not mechanic_id or not mechanic_id.startswith("MEC"):
        raise HTTPException(status_code=403, detail="Only mechanics can create progress updates")
    
    booking = await db.get(Booking, progress_data.booking_id)
    if not booking:
        raise HTTPException(status_code=404, detail="Booking not found")
    
    current_booking_status = booking.status.name.lower()
    valid_states = ["pickup", "in-progress", "out for delivery"]

    if current_booking_status not in valid_states:
        raise HTTPException(status_code=400, detail="Attempting invalid state transition")
    

    # Mark services as completed
    if current_booking_status == "in-progress" and progress_data.services_completed_ids:
        await db.execute(
            update(BookedService)
            .where(
                BookedService.booking_id == progress_data.booking_id,
                BookedService.service_id.in_(progress_data.services_completed_ids),
            )
            .values(completed=True)
        )
        
    # Create progress update
    progress = BookingProgress(
        mechanic_id=mechanic_id,
        booking_id=progress_data.booking_id,
        description=progress_data.description,
        images=progress_data.images,
        status_id=booking.status_id,
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
    """Mechanic creates analysis report"""
    mechanic_id = payload.get("user_id")
    if not mechanic_id or not mechanic_id.startswith("MEC"):
        raise HTTPException(status_code=403, detail="Only mechanics can create analysis")
    
    booking = await db.get(Booking, analysis_data.booking_id)
    if not booking:
        raise HTTPException(status_code=404, detail="Booking not found")
    
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


# Admin validation functions
async def update_progress(db: Session, progress_id: int, update_data: BookingProgressUpdate):
    """Admin updates progress"""
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
    """Admin validates progress update"""
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
    
    # if all services are completed, change booking to completed state
    if progress.status_id == await get_status_id_by_name(db, "in-progress"):
        confirmed_status_id = await get_status_id_by_name(db, "confirmed")
        print(confirmed_status_id)
        if check_all_booked_services_completed(progress.booking.booked_services, confirmed_status_id):
            print(2)
            await update_booking_status(db, progress.booking, "completed")
    
    progress.validated = True
    
    await db.commit()
    
    return JSONResponse(content={"message": "Progress validated and sent to customer"})


async def update_analysis(db: Session, booking_id: int, update_data: BookingAnalysisUpdate):
    """Admin updates analysis"""
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
    """Admin validates analysis report"""
    analysis = await db.get(BookingAnalysis, booking_id)
    if not analysis:
        raise HTTPException(status_code=404, detail="Analysis record not found")
    
    if analysis.validated:
        raise HTTPException(status_code=400, detail="Analysis already validated.")
    
    analysis.validated = True
    
    await db.commit()
    
    return JSONResponse(content={"message": "Analysis validated and sent to customer"})


# webhook function for confirming payment and booking
async def confirm_booking_webhook(db: Session, order_id: str, payment_id: str, signature: str):
    # fetch payment object
    result = await db.execute(
        select(OnlinePayment).where(OnlinePayment.razorpay_order_id == order_id)
    )
    payment = result.scalar_one_or_none()

    if not payment_service.verify_signature(order_id, payment_id, signature):
        # update payment failed
        payment.razorpay_payment_id = payment_id
        payment.razorpay_signature = signature
        payment.status_id = await get_status_id_by_name(db, "failed")
        raise HTTPException(status_code=400, detail="Invalid payment signature")
    
    # update payment success
    payment.razorpay_payment_id = payment_id
    payment.razorpay_signature = signature
    payment.status_id = await get_status_id_by_name(db, "success")

    
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
    await confirm_selected_services(db, booking, set(selection.service_ids), confirmed_status_id, rejected_status_id)
    
    # Update booking status to 'in-progress'
    await update_booking_status(db, booking, "in-progress")
       
    await db.commit()
    
    return JSONResponse(content={"message": "Payment successful."})