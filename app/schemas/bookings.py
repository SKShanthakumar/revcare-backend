from pydantic import BaseModel, Field, field_validator, model_validator
from typing import Optional, Dict, List
from datetime import date, datetime
from decimal import Decimal
from .service import ServiceInBooking
from .customer import CustomerResponse

# Address schemas for nested creation
class AddressInput(BaseModel):
    label: Optional[str] = None
    line1: str
    line2: Optional[str] = None
    area_id: int

# Booking Create
class BookingCreate(BaseModel):
    customer_car_id: int
    pickup_address_id: Optional[int] = None
    pickup_address: Optional[AddressInput] = None
    drop_address_id: Optional[int] = None
    drop_address: Optional[AddressInput] = None
    pickup_date: date
    drop_date: date
    pickup_timeslot_id: int
    drop_timeslot_id: int
    service_price: Dict[int, Decimal] = Field(..., description="Dict with service_id as key and est_price as value")

    @model_validator(mode="after")
    def validate_dates(self):
        """Ensure pickup_date < drop_date."""
        today = date.today()

        if self.pickup_date < today:
            raise ValueError("Pickup date cannot be in the past.")
        if self.pickup_date >= self.drop_date:
            raise ValueError("Pickup date must be earlier than drop date.")
        return self


# Booking Response
class BookingResponse(BaseModel):
    id: int
    customer: CustomerResponse
    car: dict
    pickup: dict
    drop: dict
    created_at: Optional[datetime]
    
    class Config:
        from_attributes = True

class BookingResponseDetailed(BaseModel):
    id: int
    status: str
    customer: CustomerResponse
    car: dict
    pickup: dict
    drop: dict
    booked_services: List[ServiceInBooking]
    booking_progress: List[dict]
    total_estimated_price: Decimal
    total_final_price: Optional[Decimal]
    created_at: Optional[datetime]
    updated_at: Optional[datetime]
    completed_at: Optional[datetime]
    payment_method: str | None


# Mechanic Assignment
class MechanicAssignmentCreate(BaseModel):
    mechanic_id: str
    booking_id: int
    assignment_type_id: int

class MechanicAssignmentResponse(BaseModel):
    id: int
    mechanic_id: str
    booking_id: int
    assignment_type_id: int
    status_id: int
    assigned_at: datetime
    
    class Config:
        from_attributes = True

class MechanicAssignmentDetailedResponse(BaseModel):
    id: int
    booking_id: int
    assignment_type: str
    status: str
    assigned_at: datetime

    class Config:
        from_attributes = True

# Booking Progress
class BookingProgressCreate(BaseModel):
    booking_id: int
    description: str
    images: List[str] = Field(..., max_length=5, description="List of image URLs")
    services_completed_ids: List[int] = Field([], description="List of service IDs from booked_services that are completed")

    @field_validator('images')
    def validate_images(cls, v:list[str]) -> list[str]:
        """Validate image URLs"""
        # Remove empty strings and duplicates
        v = list(dict.fromkeys([url.strip() for url in v if url and url.strip()]))
        
        if len(v) == 0:
            raise ValueError("Atleast 1 image is required")

        if len(v) > 5:
            raise ValueError("Maximum 5 images allowed")
        
        # Basic URL validation
        for url in v:
            if not url.startswith(('http://', 'https://', '/')):
                raise ValueError(f"Invalid image URL: {url}")
            if len(url) > 500:
                raise ValueError(f"Image URL too long: {url}")
        
        return v if v else None

class BookingProgressUpdate(BaseModel):
    description: Optional[str] = None
    images: Optional[List[str]] = None
    completed_service_ids: Optional[List[int]] = None

    @field_validator('images')
    def validate_images(cls, v: Optional[List[str]]) -> list[str] | None:
        """Validate image URLs"""
        # Remove empty strings and duplicates
        if v is None:
            return v
        
        v = list(dict.fromkeys([url.strip() for url in v if url and url.strip()]))

        if len(v) == 0:
            raise ValueError("Atleast 1 image is required")
        
        if len(v) > 5:
            raise ValueError("Maximum 5 images allowed")
        
        # Basic URL validation
        for url in v:
            if not url.startswith(('http://', 'https://', '/')):
                raise ValueError(f"Invalid image URL: {url}")
            if len(url) > 500:
                raise ValueError(f"Image URL too long: {url}")

class BookingProgressResponse(BaseModel):
    id: int
    mechanic_id: str
    booking_id: int
    description: str
    images: List[str]
    status_id: int
    validated: bool
    created_at: datetime
    
    class Config:
        from_attributes = True

# Booking Analysis
class BookingAnalysisCreate(BaseModel):
    booking_id: int
    description: str
    recommendation: str
    images: List[str] = Field(..., max_length=5, description="List of image URLs")
    price_quote: Dict[int, Decimal] = Field(..., description="Dict with service_id as key and price as value")
    recommended_services: Optional[Dict[int, Decimal]] = Field(None, description="Dict with service_id as key and price as value")

    @field_validator('images')
    def validate_images(cls, v:list[str]) -> list[str]:
        """Validate image URLs"""
        # Remove empty strings and duplicates
        v = list(dict.fromkeys([url.strip() for url in v if url and url.strip()]))

        if len(v) == 0:
            raise ValueError("Atleast 1 image is required")
        
        if len(v) > 5:
            raise ValueError("Maximum 5 images allowed")
        
        # Basic URL validation
        for url in v:
            if not url.startswith(('http://', 'https://', '/')):
                raise ValueError(f"Invalid image URL: {url}")
            if len(url) > 500:
                raise ValueError(f"Image URL too long: {url}")
        
        return v if v else None

class BookingAnalysisUpdate(BaseModel):
    description: Optional[str] = None
    recommendation: Optional[str] = None
    images: Optional[List[str]] = None

    @field_validator('images')
    def validate_images(cls, v: Optional[List[str]]) -> list[str] | None:
        """Validate image URLs"""
        # Remove empty strings and duplicates
        if v is None:
            return v
        
        v = list(dict.fromkeys([url.strip() for url in v if url and url.strip()]))

        if len(v) == 0:
            raise ValueError("Atleast 1 image is required")
        
        if len(v) > 5:
            raise ValueError("Maximum 5 images allowed")
        
        # Basic URL validation
        for url in v:
            if not url.startswith(('http://', 'https://', '/')):
                raise ValueError(f"Invalid image URL: {url}")
            if len(url) > 500:
                raise ValueError(f"Image URL too long: {url}")

class BookingAnalysisResponse(BaseModel):
    booking_id: int
    mechanic_id: str
    description: str
    recommendation: str
    images: List[str]
    validated: bool
    created_at: datetime
    
    class Config:
        from_attributes = True

# Customer Service Selection
class CustomerServiceSelection(BaseModel):
    service_ids: List[int] = Field(..., description="List of service IDs to confirm (from booked_services or booking_recommendations)")
    payment_method_id: int


# Booked Service Response
class BookedServiceResponse(BaseModel):
    booking_id: int
    service_id: int
    status_id: int
    est_price: Decimal
    price: Optional[Decimal]
    completed: bool
    created_at: datetime
    
    class Config:
        from_attributes = True

# Booking Recommendation Response
class BookingRecommendationResponse(BaseModel):
    booking_id: int
    service_id: int
    price: Decimal
    created_at: datetime
    
    class Config:
        from_attributes = True

# Admin Dashboard Data
class AdminBookingDashboard(BaseModel):
    booking_id: int
    customer_name: str
    car_model: str
    car_reg: str
    status: str
    status_id: int
    drop_date: date
    created_at: datetime
    action_required: str  # "assign", "validate", "waiting", "none"
    latest_progress: Optional[Dict] = None
    analysis_report: Optional[Dict] = None
    latest_assignment: Optional[Dict] = None

# Customer View Booking
class CustomerBookingView(BaseModel):
    id: int
    car: dict
    status: str  # "booked", "analysed", "in-progress", "completed", "delivered"
    validate_price: bool
    pickup_date: date
    drop_date: date
    created_at: datetime