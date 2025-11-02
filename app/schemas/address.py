from pydantic import BaseModel, Field, field_validator
from typing import Optional
from datetime import datetime
from .area import AreaResponse
from .customer import CustomerResponse
import re

class AddressBase(BaseModel):
    """Base schema for Address"""
    label: Optional[str] = Field(None, max_length=50, description="Label for the address (e.g., Home, Office)")
    line1: str = Field(..., min_length=1, max_length=200, description="Address line 1")
    line2: Optional[str] = Field(None, max_length=200, description="Address line 2")
    area_id: int = Field(..., gt=0, description="Area ID reference")
    
    @field_validator('label')
    def validate_label(cls, v: Optional[str]) -> Optional[str]:
        """Validate and normalize address label"""
        if v is None:
            return v
        v = v.strip()
        if not v:
            return None
        if len(v) < 2:
            raise ValueError("Address label must be at least 2 characters long")
        return v
    
    @field_validator('line1')
    def validate_line1(cls, v: str) -> str:
        """Validate and normalize address line 1"""
        v = v.strip()
        if not v:
            raise ValueError("Address line 1 cannot be empty or only whitespace")
        if len(v) < 3:
            raise ValueError("Address line 1 must be at least 3 characters long")
        return v
    
    @field_validator('line2')
    def validate_line2(cls, v: Optional[str]) -> Optional[str]:
        """Validate and normalize address line 2"""
        if v is None:
            return v
        v = v.strip()
        if not v:
            return None
        return v


class AddressCreate(AddressBase):
    """Schema for creating a new address"""
    pass


class AddressResponse(AddressBase):
    """Schema for address response"""
    id: int = Field(..., description="Unique identifier for the address")
    area: AreaResponse
    customer: CustomerResponse
    created_at: datetime = Field(..., description="Timestamp when address was created")
    
    class Config:
        from_attributes = True


class AddressUpdate(BaseModel):
    """Schema for updating an address"""
    label: Optional[str] = Field(None, max_length=50, description="Label for the address")
    line1: Optional[str] = Field(None, min_length=1, max_length=200, description="Address line 1")
    line2: Optional[str] = Field(None, max_length=200, description="Address line 2")
    area_id: Optional[int] = Field(None, gt=0, description="Area ID reference")
    
    @field_validator('label')
    def validate_label(cls, v: Optional[str]) -> Optional[str]:
        """Validate and normalize address label"""
        if v is None:
            return v
        v = v.strip()
        if not v:
            raise ValueError("Address label cannot be empty or only whitespace")
        if len(v) < 2:
            raise ValueError("Address label must be at least 2 characters long")
        return v
    
    @field_validator('line1')
    def validate_line1(cls, v: Optional[str]) -> Optional[str]:
        """Validate and normalize address line 1"""
        if v is None:
            return v
        v = v.strip()
        if not v:
            raise ValueError("Address line 1 cannot be empty or only whitespace")
        if len(v) < 3:
            raise ValueError("Address line 1 must be at least 3 characters long")
        return v
    
    @field_validator('line2')
    def validate_line2(cls, v: Optional[str]) -> Optional[str]:
        """Validate and normalize address line 2"""
        if v is None:
            return v
        v = v.strip()
        if not v:
            return None  # Allow clearing line2
        return v
