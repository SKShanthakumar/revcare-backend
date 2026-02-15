from fastapi import APIRouter, Depends, Security, BackgroundTasks
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession as Session
from typing import List, Optional
from app.database.dependencies import get_postgres_db
from app.schemas import (
    BookingCreate, BookingResponse, MechanicAssignmentCreate, 
    MechanicAssignmentResponse, BookingProgressCreate, BookingProgressUpdate,
    BookingProgressResponse, BookingAnalysisCreate, BookingAnalysisUpdate,
    BookingAnalysisResponse, CustomerServiceSelection,
    AdminBookingDashboard, CustomerBookingView, BookingResponseDetailed,
    MechanicAssignmentDetailedResponse
)
from app.services import bookings as booking_service
from app.auth.dependencies import validate_token

router = APIRouter()

# Customer Endpoints
@router.post("/", response_model=BookingResponse)
async def create_booking(
    booking: BookingCreate,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_postgres_db),
    payload = Security(validate_token, scopes=["WRITE:BOOKINGS"])
):
    """
    Create a new booking.
    
    Args:
        booking: Booking creation data
        db: Database session
        payload: Validated token payload
        
    Returns:
        BookingResponse: Created booking information
    """
    return await booking_service.create_booking(db, booking, payload, background_tasks)


@router.get("/customer", response_model=List[CustomerBookingView])
async def get_customer_bookings(
    db: Session = Depends(get_postgres_db),
    payload = Security(validate_token, scopes=["READ:BOOKINGS"])
):
    """
    Get all bookings for logged-in customer.
    
    Args:
        db: Database session
        payload: Validated token payload
        
    Returns:
        List[CustomerBookingView]: List of customer bookings with simplified status
    """
    return await booking_service.get_customer_bookings(db, payload)


@router.put("/{booking_id}/confirm-services", response_class=JSONResponse)
async def confirm_services(
    booking_id: int,
    selection: CustomerServiceSelection,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_postgres_db),
    payload = Security(validate_token, scopes=["UPDATE:BOOKINGS"])
):
    """
    Confirm selected services after analysis.
    
    Args:
        booking_id: Booking ID
        selection: Service selection with payment method
        db: Database session
        payload: Validated token payload
        
    Returns:
        JSONResponse: Payment order details or success message
    """
    return await booking_service.customer_confirm_services(db, booking_id, selection, payload, background_tasks)


@router.put("/{booking_id}/cancel", response_class=JSONResponse)
async def cancel_booking(
    booking_id: int,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_postgres_db),
    payload = Security(validate_token, scopes=["UPDATE:BOOKINGS"])
):
    """
    Cancel a booking.
    
    Args:
        booking_id: Booking ID to cancel
        db: Database session
        payload: Validated token payload
        
    Returns:
        JSONResponse: Success message with cancellation fee
    """
    return await booking_service.cancel_booking(db, booking_id, payload, background_tasks)


# Admin Endpoints
@router.get("/admin/dashboard", response_model=List[AdminBookingDashboard])
async def get_admin_bookings_dashboard(
    status_id: Optional[int] = None,
    action_required: Optional[str] = None,
    db: Session = Depends(get_postgres_db),
    payload = Security(validate_token, scopes=["READ:BOOKINGS", "READ:BOOKING_ASSIGNMENT"])
):
    """
    Get all bookings with action indicators for admin dashboard.
    
    Args:
        status_id: Optional status ID to filter by
        action_required: Optional action type filter
        db: Database session
        payload: Validated token payload
        
    Returns:
        List[AdminBookingDashboard]: List of bookings with action indicators
    """
    return await booking_service.get_admin_dashboard_bookings(db, payload, status_id, action_required)


@router.post("/admin/assign", response_model=MechanicAssignmentResponse)
async def assign_mechanic(
    assignment: MechanicAssignmentCreate,
    db: Session = Depends(get_postgres_db),
    payload = Security(validate_token, scopes=["WRITE:BOOKING_ASSIGNMENT"])
):
    """
    Assign a mechanic to a booking.
    
    Args:
        assignment: Assignment data
        db: Database session
        payload: Validated token payload
        
    Returns:
        MechanicAssignmentResponse: Created assignment information
    """
    return await booking_service.assign_mechanic(db, assignment)


@router.put("/admin/progress/{progress_id}", response_model=BookingProgressResponse)
async def update_progress(
    progress_id: int,
    update_data: BookingProgressUpdate,
    db: Session = Depends(get_postgres_db),
    payload = Security(validate_token, scopes=["UPDATE:BOOKING_PROGRESS"])
):
    """
    Update a progress record (admin edit).
    
    Args:
        progress_id: Progress record ID
        update_data: Updated progress data
        db: Database session
        payload: Validated token payload
        
    Returns:
        BookingProgressResponse: Updated progress record
    """
    return await booking_service.update_progress(db, progress_id, update_data)


@router.post("/admin/progress/{progress_id}/validate", response_class=JSONResponse)
async def validate_progress(
    progress_id: int,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_postgres_db),
    payload = Security(validate_token, scopes=["UPDATE:BOOKING_PROGRESS"])
):
    """
    Validate and approve a progress update.
    
    Args:
        progress_id: Progress record ID
        db: Database session
        payload: Validated token payload
        
    Returns:
        JSONResponse: Success message
    """
    return await booking_service.validate_progress(db, progress_id, background_tasks)


@router.put("/admin/analysis/{booking_id}", response_model=BookingAnalysisResponse)
async def update_analysis(
    booking_id: int,
    update_data: BookingAnalysisUpdate,
    db: Session = Depends(get_postgres_db),
    payload = Security(validate_token, scopes=["UPDATE:BOOKING_ANALYSIS"])
):
    """
    Update an analysis report (admin edit).
    
    Args:
        booking_id: Booking ID
        update_data: Updated analysis data
        db: Database session
        payload: Validated token payload
        
    Returns:
        BookingAnalysisResponse: Updated analysis record
    """
    return await booking_service.update_analysis(db, booking_id, update_data)


@router.post("/admin/analysis/{booking_id}/validate", response_class=JSONResponse)
async def validate_analysis(
    booking_id: int,
    db: Session = Depends(get_postgres_db),
    payload = Security(validate_token, scopes=["UPDATE:BOOKING_ANALYSIS"])
):
    """
    Validate and approve an analysis report.
    
    Args:
        booking_id: Booking ID
        db: Database session
        payload: Validated token payload
        
    Returns:
        JSONResponse: Success message
    """
    return await booking_service.validate_analysis(db, booking_id)


# Mechanic Endpoints
@router.get("/mechanic/assignments", response_model=List[MechanicAssignmentDetailedResponse])
async def get_mechanic_assignments(
    db: Session = Depends(get_postgres_db),
    payload = Security(validate_token, scopes=["READ:BOOKING_ASSIGNMENT"])
):
    """
    Get all assignments for logged-in mechanic.
    
    Args:
        db: Database session
        payload: Validated token payload
        
    Returns:
        List[MechanicAssignmentDetailedResponse]: List of mechanic assignments
    """
    return await booking_service.get_mechanic_assignments(db, payload)


@router.post("/mechanic/progress", response_model=BookingProgressResponse)
async def create_progress_update(
    progress: BookingProgressCreate,
    db: Session = Depends(get_postgres_db),
    payload = Security(validate_token, scopes=["WRITE:BOOKING_PROGRESS"])
):
    """
    Create a progress update.
    
    Args:
        progress: Progress update data
        db: Database session
        payload: Validated token payload
        
    Returns:
        BookingProgressResponse: Created progress update
    """
    return await booking_service.create_progress_update(db, progress, payload)


@router.post("/mechanic/analysis", response_model=BookingAnalysisResponse)
async def create_analysis(
    analysis: BookingAnalysisCreate,
    db: Session = Depends(get_postgres_db),
    payload = Security(validate_token, scopes=["WRITE:BOOKING_ANALYSIS"])
):
    """
    Create an analysis report.
    
    Args:
        analysis: Analysis data
        db: Database session
        payload: Validated token payload
        
    Returns:
        BookingAnalysisResponse: Created analysis report
    """
    return await booking_service.create_analysis(db, analysis, payload)


# common endpoints
@router.get("/{booking_id}", response_model=BookingResponseDetailed)
async def get_booking_details(
    booking_id: int,
    db: Session = Depends(get_postgres_db),
    payload = Security(validate_token, scopes=["READ:BOOKINGS", "READ:BOOKED_SERVICES"])
):
    """
    Get detailed booking information.
    
    Args:
        booking_id: Booking ID
        db: Database session
        payload: Validated token payload
        
    Returns:
        BookingResponseDetailed: Detailed booking information
    """
    return await booking_service.get_booking_by_id(db, booking_id, payload)