from pydantic import BaseModel, Field, field_validator
from typing import Optional

class AreaBase(BaseModel):
    """Base schema for Area"""
    name: str = Field(..., min_length=1, max_length=100, description="Name of the area")

    @field_validator('name')
    def validate_name(cls, v: str) -> str:
        """Validate and normalize area name"""
        v = v.strip()
        if not v:
            raise ValueError("Area name cannot be empty or only whitespace")
        if len(v) < 2:
            raise ValueError("Area name must be at least 2 characters long")
        return v


class AreaCreate(AreaBase):
    """Schema for creating a new area"""
    pass


class AreaResponse(AreaBase):
    """Schema for area response"""
    id: int = Field(..., description="Unique identifier for the area")

    class Config:
        from_attributes = True
        

class AreaUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=100, description="Name of the area")

    @field_validator('name')
    def validate_name(cls, v: str) -> str:
        """Validate and normalize area name"""
        if v is None:
            return v 
        v = v.strip()
        if not v:
            raise ValueError("Area name cannot be empty or only whitespace")
        if len(v) < 2:
            raise ValueError("Area name must be at least 2 characters long")
        return v
