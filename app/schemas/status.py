from pydantic import BaseModel, Field, field_validator
from typing import Optional

class StatusBase(BaseModel):
    """Base schema for status"""
    name: str = Field(..., min_length=1, max_length=100, description="Name of the status")

    @field_validator('name')
    def validate_name(cls, v: str) -> str:
        """Validate and normalize status name"""
        v = v.strip()
        if not v:
            raise ValueError("Status name cannot be empty or only whitespace")
        if len(v) < 2:
            raise ValueError("Status name must be at least 2 characters long")
        return v


class StatusCreate(StatusBase):
    """Schema for creating a new status"""
    pass


class StatusResponse(StatusBase):
    """Schema for status response"""
    id: int = Field(..., description="Unique identifier for the status")

    class Config:
        from_attributes = True

class StatusUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=100, description="Name of the status")

    @field_validator('name')
    def validate_name(cls, v: str) -> str:
        """Validate and normalize status name"""
        if v is None:
            return v 
        v = v.strip()
        if not v:
            raise ValueError("Status name cannot be empty or only whitespace")
        if len(v) < 2:
            raise ValueError("Status name must be at least 2 characters long")
        return v