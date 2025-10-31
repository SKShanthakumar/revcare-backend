from pydantic import BaseModel, Field, field_validator
from typing import Optional
from datetime import datetime
from .manufacturer import ManufacturerResponse
from .fuel_type import FuelTypeResponse
from .car_class import CarClassResponse

class CarBase(BaseModel):
    """Base schema for Car"""
    model: str = Field(..., min_length=1, max_length=100, description="Car model name")
    manufacturer_id: int = Field(..., gt=0, description="ID of the manufacturer")
    fuel_type_id: int = Field(..., gt=0, description="ID of the fuel type")
    car_class_id: int = Field(..., gt=0, description="ID of the car class")
    year: int = Field(..., ge=1900, le=2100, description="Manufacturing year")
    img: str = Field(..., min_length=1, max_length=255, description="Image path or URL")

    @field_validator('model')
    def validate_model(cls, v: str) -> str:
        """Validate and normalize car model name"""
        v = v.strip()
        if not v:
            raise ValueError("Car model cannot be empty or only whitespace")
        return v

    @field_validator('img')
    def validate_img(cls, v: str) -> str:
        """Validate image path"""
        v = v.strip()
        if not v:
            raise ValueError("Image path cannot be empty or only whitespace")
        return v

    @field_validator('year')
    def validate_year(cls, v: int) -> int:
        """Validate manufacturing year"""
        current_year = datetime.now().year
        if v > current_year + 1:
            raise ValueError(f"Manufacturing year cannot be more than {current_year + 1}")
        if v < 1900:
            raise ValueError("Manufacturing year must be 1900 or later")
        return v


class CarCreate(CarBase):
    """Schema for creating a new car"""
    pass


class CarResponse(CarBase):
    """Schema for car response with relationships"""
    id: int = Field(..., description="Unique identifier for the car")
    manufacturer: Optional[ManufacturerResponse] = None
    fuel_type: Optional[FuelTypeResponse] = None
    car_class: Optional[CarClassResponse] = None

    class Config:
        from_attributes = True
