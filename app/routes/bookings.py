from fastapi import APIRouter, Depends, Security, HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession as Session
from typing import List, Optional
from app.database.dependencies import get_postgres_db
from app.schemas import (
    BookingCreate, BookingResponse, MechanicAssignmentCreate, 
    MechanicAssignmentResponse, BookingProgressCreate, BookingProgressUpdate,
    BookingProgressResponse, BookingAnalysisCreate, BookingAnalysisUpdate,
    BookingAnalysisResponse, CustomerServiceSelection,
    BookedServiceResponse, AdminBookingDashboard, CustomerBookingView, BookingResponseDetailed,
    MechanicAssignmentDetailedResponse
)
from app.services import bookings as booking_service
from app.auth.dependencies import validate_token

router = APIRouter()

# Customer Endpoints
@router.post("/", response_model=BookingResponse)
async def create_booking(
    booking: BookingCreate,
    db: Session = Depends(get_postgres_db),
    payload = Security(validate_token, scopes=["WRITE:BOOKINGS"])
):
    """Customer creates a new booking"""
    return await booking_service.create_booking(db, booking, payload)


@router.get("/customer", response_model=List[CustomerBookingView])
async def get_customer_bookings(
    db: Session = Depends(get_postgres_db),
    payload = Security(validate_token, scopes=["READ:BOOKINGS"])
):
    """Get all bookings for logged-in customer with simplified status"""
    return await booking_service.get_customer_bookings(db, payload)


@router.put("/{booking_id}/confirm-services", response_class=JSONResponse)
async def confirm_services(
    booking_id: int,
    selection: CustomerServiceSelection,
    db: Session = Depends(get_postgres_db),
    payload = Security(validate_token, scopes=["UPDATE:BOOKINGS"])
):
    """Customer confirms which services to proceed with after analysis"""
    return await booking_service.customer_confirm_services(db, booking_id, selection, payload)


@router.put("/{booking_id}/cancel", response_class=JSONResponse)
async def cancel_booking(
    booking_id: int,
    db: Session = Depends(get_postgres_db),
    payload = Security(validate_token, scopes=["UPDATE:BOOKINGS"])
):
    """Customer cancels a booking"""
    return await booking_service.cancel_booking(db, booking_id, payload)


# Admin Endpoints
@router.get("/admin/dashboard", response_model=List[AdminBookingDashboard])
async def get_admin_bookings_dashboard(
    status_id: Optional[int] = None,
    action_required: Optional[str] = None,
    db: Session = Depends(get_postgres_db),
    payload = Security(validate_token, scopes=["READ:BOOKINGS", "READ:BOOKING_ASSIGNMENT"])
):
    """Get all bookings with action indicators for admin dashboard"""
    return await booking_service.get_admin_dashboard_bookings(db, payload, status_id, action_required)


@router.post("/admin/assign", response_model=MechanicAssignmentResponse)
async def assign_mechanic(
    assignment: MechanicAssignmentCreate,
    db: Session = Depends(get_postgres_db),
    payload = Security(validate_token, scopes=["WRITE:BOOKING_ASSIGNMENT"])
):
    """Admin assigns mechanic to a booking"""
    return await booking_service.assign_mechanic(db, assignment)


@router.put("/admin/progress/{progress_id}", response_model=BookingProgressResponse)
async def update_progress(
    progress_id: int,
    update_data: BookingProgressUpdate,
    db: Session = Depends(get_postgres_db),
    payload = Security(validate_token, scopes=["UPDATE:BOOKING_PROGRESS"])
):
    """Admin edits progress update"""
    return await booking_service.update_progress(db, progress_id, update_data)


@router.post("/admin/progress/{progress_id}/validate", response_class=JSONResponse)
async def validate_progress(
    progress_id: int,
    db: Session = Depends(get_postgres_db),
    payload = Security(validate_token, scopes=["UPDATE:BOOKING_PROGRESS"])
):
    """Admin validates and approves progress update"""
    return await booking_service.validate_progress(db, progress_id)


@router.put("/admin/analysis/{booking_id}", response_model=BookingAnalysisResponse)
async def update_analysis(
    booking_id: int,
    update_data: BookingAnalysisUpdate,
    db: Session = Depends(get_postgres_db),
    payload = Security(validate_token, scopes=["UPDATE:BOOKING_ANALYSIS"])
):
    """Admin edits analysis report"""
    return await booking_service.update_analysis(db, booking_id, update_data)


@router.post("/admin/analysis/{booking_id}/validate", response_class=JSONResponse)
async def validate_analysis(
    booking_id: int,
    db: Session = Depends(get_postgres_db),
    payload = Security(validate_token, scopes=["UPDATE:BOOKING_ANALYSIS"])
):
    """Admin validates and approves analysis report"""
    return await booking_service.validate_analysis(db, booking_id)


# Mechanic Endpoints
@router.get("/mechanic/assignments", response_model=List[MechanicAssignmentDetailedResponse])
async def get_mechanic_assignments(
    db: Session = Depends(get_postgres_db),
    payload = Security(validate_token, scopes=["READ:BOOKING_ASSIGNMENT"])
):
    """Get all assignments for logged-in mechanic"""
    return await booking_service.get_mechanic_assignments(db, payload)


@router.post("/mechanic/progress", response_model=BookingProgressResponse)
async def create_progress_update(
    progress: BookingProgressCreate,
    db: Session = Depends(get_postgres_db),
    payload = Security(validate_token, scopes=["WRITE:BOOKING_PROGRESS"])
):
    """Mechanic creates progress update (pickup/drop received)"""
    return await booking_service.create_progress_update(db, progress, payload)


@router.post("/mechanic/analysis", response_model=BookingAnalysisResponse)
async def create_analysis(
    analysis: BookingAnalysisCreate,
    db: Session = Depends(get_postgres_db),
    payload = Security(validate_token, scopes=["WRITE:BOOKING_ANALYSIS"])
):
    """Mechanic creates analysis report"""
    return await booking_service.create_analysis(db, analysis, payload)


# common endpoints
@router.get("/{booking_id}", response_model=BookingResponseDetailed)
async def get_booking_details(
    booking_id: int,
    db: Session = Depends(get_postgres_db),
    payload = Security(validate_token, scopes=["READ:BOOKINGS", "READ:BOOKED_SERVICES"])
):
    """Get detailed booking information"""
    return await booking_service.get_booking_by_id(db, booking_id, payload)