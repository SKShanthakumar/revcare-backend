from pydantic import BaseModel, Field, field_validator
from typing import Optional

class ServiceCategoryBase(BaseModel):
    """Base schema for Service Category"""
    name: str = Field(..., min_length=1, max_length=100, description="Name of the service category")
    description: str = Field(..., min_length=1, max_length=100, description="Description of the service category")

    @field_validator('name')
    def validate_name(cls, v: str) -> str:
        """Validate and normalize service category name"""
        v = v.strip()
        if not v:
            raise ValueError("Service category name cannot be empty or only whitespace")
        if len(v) < 2:
            raise ValueError("Service category name must be at least 2 characters long")
        return v
    
    @field_validator('description')
    def validate_description(cls, v: str) -> str:
        """Validate and normalize service category description"""
        v = v.strip()
        if not v:
            raise ValueError("Service category description cannot be empty or only whitespace")
        if len(v.split()) < 2:
            raise ValueError("Service category description must be at least 2 words long")
        return v


class ServiceCategoryCreate(ServiceCategoryBase):
    """Schema for creating a new service category"""
    pass


class ServiceCategoryResponse(ServiceCategoryBase):
    """Schema for service category response"""
    id: int = Field(..., description="Unique identifier for the service category")

    class Config:
        from_attributes = True

class ServiceCategoryUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=100, description="Name of the service category")
    description: Optional[str] = Field(None, min_length=1, max_length=100, description="Description of the service category")

    @field_validator('name')
    def validate_name(cls, v: str) -> str:
        """Validate and normalize service category name"""
        if v is None:
            return v 
        v = v.strip()
        if not v:
            raise ValueError("Service category name cannot be empty or only whitespace")
        if len(v) < 2:
            raise ValueError("Service category name must be at least 2 characters long")
        return v
    
    @field_validator('description')
    def validate_description(cls, v: str) -> str:
        """Validate and normalize service category description"""
        if v is None:
            return v 
        v = v.strip()
        if not v:
            raise ValueError("Service category description cannot be empty or only whitespace")
        if len(v.split()) < 2:
            raise ValueError("Service category description must be at least 2 words long")
        return v