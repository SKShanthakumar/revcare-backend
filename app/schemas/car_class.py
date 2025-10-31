from pydantic import BaseModel, Field, field_validator
from typing import Optional

class CarClassBase(BaseModel):
    """Base schema for CarClass"""
    class_: str = Field(..., min_length=1, max_length=50, description="Car class category", alias="class")

    @field_validator('class_')
    def validate_class(cls, v: str) -> str:
        """Validate and normalize car class"""
        v = v.strip()
        if not v:
            raise ValueError("Car class cannot be empty or only whitespace")
        return v

class CarClassCreate(CarClassBase):
    """Schema for creating a new car class"""
    pass

class CarClassResponse(CarClassBase):
    """Schema for car class response"""
    id: int = Field(..., description="Unique identifier for the car class")

    class Config:
        from_attributes = True
        populate_by_name = True

class CarClassUpdate(BaseModel):
    """Base schema for CarClass"""
    class_: Optional[str] = Field(None, min_length=1, max_length=50, description="Car class category", alias="class")

    @field_validator('class_')
    def validate_class(cls, v: str) -> str:
        """Validate and normalize car class"""
        if v is None:
            return v 
        v = v.strip()
        if not v:
            raise ValueError("Car class cannot be empty or only whitespace")
        return v