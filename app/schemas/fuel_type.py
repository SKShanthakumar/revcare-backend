from pydantic import BaseModel, Field, field_validator
from typing import Optional

class FuelTypeBase(BaseModel):
    """Base schema for FuelType"""
    fuel_name: str = Field(..., min_length=1, max_length=50, description="Name of the fuel type")

    @field_validator('fuel_name')
    def validate_fuel_name(cls, v: str) -> str:
        """Validate and normalize fuel name"""
        v = v.strip()
        if not v:
            raise ValueError("Fuel name cannot be empty or only whitespace")
        return v


class FuelTypeCreate(FuelTypeBase):
    """Schema for creating a new fuel type"""
    pass


class FuelTypeResponse(FuelTypeBase):
    """Schema for fuel type response"""
    id: int = Field(..., description="Unique identifier for the fuel type")

    class Config:
        from_attributes = True

class FuelTypeUpdate(BaseModel):
    """Base schema for FuelType"""
    fuel_name: Optional[str] = Field(None, min_length=1, max_length=50, description="Name of the fuel type")

    @field_validator('fuel_name')
    def validate_fuel_name(cls, v: str) -> str:
        """Validate and normalize fuel name"""
        if v is None:
            return v 
        v = v.strip()
        if not v:
            raise ValueError("Fuel name cannot be empty or only whitespace")
        return v
