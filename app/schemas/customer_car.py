from pydantic import BaseModel, Field, field_validator
from typing import Optional
from datetime import datetime
import re
from .customer import CustomerResponse
from .car import CarResponse

class CustomerCarBase(BaseModel):
    """Base schema for CustomerCar"""
    reg_number: str = Field(..., min_length=1, max_length=20, description="Vehicle registration number")
    car_model_id: int = Field(..., gt=0, description="ID of the car model")
    customer_id: str = Field(..., min_length=1, max_length=20, description="ID of the customer")

    @field_validator('reg_number')
    def validate_reg_number(cls, v: str) -> str:
        """Validate and normalize registration number"""
        v = v.strip().upper()  # Convert to uppercase and remove whitespace
        if not v:
            raise ValueError("Registration number cannot be empty or only whitespace")
        
        # Remove spaces and hyphens for validation
        clean_reg = re.sub(r'[\s\-]', '', v)
        
        # Basic validation - alphanumeric only
        if not re.match(r'^[A-Z0-9]+$', clean_reg):
            raise ValueError("Registration number can only contain letters and numbers")
        
        if len(clean_reg) < 4:
            raise ValueError("Registration number must be at least 4 characters long")
        
        return v

    @field_validator('customer_id')
    def validate_customer_id(cls, v: str) -> str:
        """Validate customer ID format"""
        v = v.strip()
        if not v:
            raise ValueError("Customer ID cannot be empty")
        # Assuming format like CST000001
        if not re.match(r'^CST\d{6}$', v):
            raise ValueError("Customer ID must be in format CST followed by 6 digits")
        return v


class CustomerCarCreate(CustomerCarBase):
    """Schema for creating a new customer car"""
    pass


class CustomerCarResponse(CustomerCarBase):
    """Schema for customer car response with relationships"""
    id: int = Field(..., description="Unique identifier for the car")
    created_at: datetime = Field(..., description="Timestamp when the car was added")
    customer: Optional[CustomerResponse] = None
    car: Optional[CarResponse] = None

    class Config:
        from_attributes = True


class CustomerCarUpdate(BaseModel):
    """Base schema for CustomerCar"""
    reg_number: Optional[str] = Field(None, min_length=1, max_length=20, description="Vehicle registration number")
    car_model_id: Optional[int] = Field(None, gt=0, description="ID of the car model")
    customer_id: Optional[str] = Field(None, min_length=1, max_length=20, description="ID of the customer")

    @field_validator('reg_number')
    def validate_reg_number(cls, v: str) -> str:
        """Validate and normalize registration number"""
        if v is None:
            return v
        v = v.strip().upper()  # Convert to uppercase and remove whitespace
        if not v:
            raise ValueError("Registration number cannot be empty or only whitespace")
        
        # Remove spaces and hyphens for validation
        clean_reg = re.sub(r'[\s\-]', '', v)
        
        # Basic validation - alphanumeric only
        if not re.match(r'^[A-Z0-9]+$', clean_reg):
            raise ValueError("Registration number can only contain letters and numbers")
        
        if len(clean_reg) < 4:
            raise ValueError("Registration number must be at least 4 characters long")
        
        return v

    @field_validator('customer_id')
    def validate_customer_id(cls, v: str) -> str:
        """Validate customer ID format"""
        if v is None:
            return v
        v = v.strip()
        if not v:
            raise ValueError("Customer ID cannot be empty")
        # Assuming format like CST000001
        if not re.match(r'^CST\d{6}$', v):
            raise ValueError("Customer ID must be in format CST followed by 6 digits")
        return v
