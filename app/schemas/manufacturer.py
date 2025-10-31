from pydantic import BaseModel, Field, field_validator
from typing import Optional

class ManufacturerBase(BaseModel):
    """Base schema for Manufacturer"""
    name: str = Field(..., min_length=1, max_length=100, description="Name of the manufacturer")

    @field_validator('name')
    def validate_name(cls, v: str) -> str:
        """Validate and normalize manufacturer name"""
        v = v.strip()
        if not v:
            raise ValueError("Manufacturer name cannot be empty or only whitespace")
        if len(v) < 2:
            raise ValueError("Manufacturer name must be at least 2 characters long")
        return v


class ManufacturerCreate(ManufacturerBase):
    """Schema for creating a new manufacturer"""
    pass


class ManufacturerResponse(ManufacturerBase):
    """Schema for manufacturer response"""
    id: int = Field(..., description="Unique identifier for the manufacturer")

    class Config:
        from_attributes = True

class ManufacturerUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=100, description="Name of the manufacturer")

    @field_validator('name')
    def validate_name(cls, v: str) -> str:
        """Validate and normalize manufacturer name"""
        if v is None:
            return v 
        v = v.strip()
        if not v:
            raise ValueError("Manufacturer name cannot be empty or only whitespace")
        if len(v) < 2:
            raise ValueError("Manufacturer name must be at least 2 characters long")
        return v