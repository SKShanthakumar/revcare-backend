from pydantic import BaseModel, Field, field_validator
from typing import Optional, List
from datetime import datetime
from decimal import Decimal
from .service_category import ServiceCategoryResponse
from .fuel_type import FuelTypeResponse
from .price_chart import PriceChartCreateWithService, PriceChartResponseWithService

class ServiceBase(BaseModel):
    """Base schema for Service"""
    title: str = Field(..., min_length=1, max_length=200, description="Name of the service")
    description: str = Field(..., max_length=1000, description="Detailed service description")
    works: List[str] = Field(..., description="List of work steps involved")
    warranty_kms: int = Field(..., ge=0, description="Warranty in kilometers")
    warranty_months: int = Field(..., ge=0, description="Warranty in months")
    time_hrs: Decimal = Field(..., ge=0, le=999.99, description="Expected service time in hours")
    difficulty: int = Field(..., ge=1, le=5, description="Difficulty level (1-5)")
    
    @field_validator('title')
    def validate_title(cls, v: str) -> str:
        """Validate and normalize service title"""
        v = v.strip()
        if not v:
            raise ValueError("Service title cannot be empty or only whitespace")
        if len(v) < 3:
            raise ValueError("Service title must be at least 3 characters long")
        return v
    
    @field_validator('description')
    def validate_description(cls, v: str) -> str:
        """Validate and normalize service description"""
        v = v.strip()
        if not v:
            raise ValueError("Service description cannot be empty or only whitespace")
        if len(v.split()) < 3:
            raise ValueError("Service description must be at least 3 words long")
        return v
    
    @field_validator('works')
    def validate_works(cls, v: List[str]) -> List[str]:
        """Validate and normalize work steps"""
        if not v:
            raise ValueError("Works list cannot be empty if provided")
        # Strip whitespace from each work step and filter out empty strings
        cleaned_works = [work.strip() for work in v if work.strip()]
        if not cleaned_works:
            raise ValueError("Works list must contain at least one non-empty work step")
        return cleaned_works
    
    @field_validator('time_hrs')
    def validate_time_hrs(cls, v: Decimal) -> Decimal:
        """Validate service time"""
        if v <= 0:
            raise ValueError("Service time must be greater than 0")
        return v


class ServiceCreate(ServiceBase):
    """Schema for creating a new service"""
    category_id: int = Field(..., gt=0, description="Service category reference")
    price_chart: List[PriceChartCreateWithService] = Field(..., description="Price for each car class")
    fuel_type_ids: List[int] = Field(..., description="Compatible fuel type ids")


class ServiceResponse(ServiceBase):
    """Schema for service response"""
    id: int = Field(..., description="Unique identifier for the service")
    category: ServiceCategoryResponse = Field(..., description="Service category details")
    price_chart: List[PriceChartResponseWithService] = Field(..., description="Price for each car class")
    fuel_types: List[FuelTypeResponse] = Field(..., description="Compatible fuel type dicts")
    created_at: datetime = Field(..., description="Record creation timestamp")
    
    class Config:
        from_attributes = True


class ServiceUpdate(BaseModel):
    """Schema for updating a service"""
    title: Optional[str] = Field(None, min_length=1, max_length=200, description="Name of the service")
    description: Optional[str] = Field(None, max_length=1000, description="Detailed service description")
    category_id: Optional[int] = Field(None, gt=0, description="Service category reference")
    works: Optional[List[str]] = Field(None, description="List of work steps involved")
    warranty_kms: Optional[int] = Field(None, ge=0, description="Warranty in kilometers")
    warranty_months: Optional[int] = Field(None, ge=0, description="Warranty in months")
    time_hrs: Optional[Decimal] = Field(None, ge=0, le=999.99, description="Expected service time in hours")
    difficulty: Optional[int] = Field(None, ge=1, le=5, description="Difficulty level (1-5)")
    
    @field_validator('title')
    def validate_title(cls, v: Optional[str]) -> Optional[str]:
        """Validate and normalize service title"""
        if v is None:
            return v
        v = v.strip()
        if not v:
            raise ValueError("Service title cannot be empty or only whitespace")
        if len(v) < 3:
            raise ValueError("Service title must be at least 3 characters long")
        return v
    
    @field_validator('description')
    def validate_description(cls, v: Optional[str]) -> Optional[str]:
        """Validate and normalize service description"""
        if v is None:
            return v
        v = v.strip()
        if not v:
            raise ValueError("Service description cannot be empty or only whitespace")
        if len(v.split()) < 3:
            raise ValueError("Service description must be at least 3 words long")
        return v
    
    @field_validator('works')
    def validate_works(cls, v: Optional[List[str]]) -> Optional[List[str]]:
        """Validate and normalize work steps"""
        if v is None:
            return v
        if not v:
            raise ValueError("Works list cannot be empty if provided")
        # Strip whitespace from each work step and filter out empty strings
        cleaned_works = [work.strip() for work in v if work.strip()]
        if not cleaned_works:
            raise ValueError("Works list must contain at least one non-empty work step")
        return cleaned_works
    
    @field_validator('time_hrs')
    def validate_time_hrs(cls, v: Optional[Decimal]) -> Optional[Decimal]:
        """Validate service time"""
        if v is not None and v <= 0:
            raise ValueError("Service time must be greater than 0")
        return v
    
    class Config:
        extra = "ignore"

class ServiceUpdateWithForeignData(ServiceUpdate):
    price_chart: Optional[List[PriceChartCreateWithService]] = Field(None, description="Price for each car class")
    fuel_type_ids: Optional[List[int]] = Field(None, description="Compatible fuel type ids")
