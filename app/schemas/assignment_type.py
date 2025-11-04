from pydantic import BaseModel, Field, field_validator
from typing import Optional

class AssignmentTypeBase(BaseModel):
    """Base schema for assignment type"""
    name: str = Field(..., min_length=1, max_length=100, description="Name of the assignment type")

    @field_validator('name')
    def validate_name(cls, v: str) -> str:
        """Validate and normalize assignment type name"""
        v = v.strip()
        if not v:
            raise ValueError("Assignment type name cannot be empty or only whitespace")
        if len(v) < 2:
            raise ValueError("Assignment type name must be at least 2 characters long")
        return v


class AssignmentTypeCreate(AssignmentTypeBase):
    """Schema for creating a new assignment type"""
    pass


class AssignmentTypeResponse(AssignmentTypeBase):
    """Schema for assignment type response"""
    id: int = Field(..., description="Unique identifier for the assignment type")

    class Config:
        from_attributes = True

class AssignmentTypeUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=100, description="Name of the assignment type")

    @field_validator('name')
    def validate_name(cls, v: str) -> str:
        """Validate and normalize assignment type name"""
        if v is None:
            return v 
        v = v.strip()
        if not v:
            raise ValueError("Assignment type name cannot be empty or only whitespace")
        if len(v) < 2:
            raise ValueError("Assignment type name must be at least 2 characters long")
        return v