from pydantic import BaseModel, Field, field_validator, model_validator
from datetime import time
from typing import Optional

class TimeslotBase(BaseModel):
    """Base schema for Timeslot"""
    name: str = Field(..., min_length=1, max_length=100, description="Name of the timeslot")
    start_time: time = Field(..., example="08:00:00")
    end_time: time = Field(..., example="10:00:00")

    @field_validator('name')
    def validate_name(cls, v: str) -> str:
        """Validate and normalize timeslot name"""
        v = v.strip()
        if not v:
            raise ValueError("Timeslot name cannot be empty or only whitespace")
        if len(v) < 2:
            raise ValueError("Timeslot name must be at least 2 characters long")
        return v
    
    @model_validator(mode="after")
    def validate_times(cls, values):
        """Ensure that end_time is after start_time"""
        start = values.start_time
        end = values.end_time

        if end <= start:
            raise ValueError("end_time must be after start_time")
        return values


class TimeslotCreate(TimeslotBase):
    """Schema for creating a new timeslot"""
    pass


class TimeslotResponse(TimeslotBase):
    """Schema for timeslot response"""
    id: int = Field(..., description="Unique identifier for the timeslot")

    class Config:
        from_attributes = True

class TimeslotUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=100, description="Name of the timeslot")
    start_time: Optional[time] = Field(None, example="08:00:00")
    end_time: Optional[time] = Field(None, example="10:00:00")

    @field_validator('name')
    def validate_name(cls, v: str) -> str:
        """Validate and normalize timeslot name"""
        if v is None:
            return v 
        v = v.strip()
        if not v:
            raise ValueError("Timeslot name cannot be empty or only whitespace")
        if len(v) < 2:
            raise ValueError("Timeslot name must be at least 2 characters long")
        return v
    
    @model_validator(mode="after")
    def validate_times(cls, values):
        """Ensure that end_time is after start_time"""
        start = values.start_time
        end = values.end_time

        if not start or not end:
            return values

        if end <= start:
            raise ValueError("end_time must be after start_time")
        return values