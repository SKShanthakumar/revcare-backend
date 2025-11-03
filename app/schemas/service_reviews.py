# Pydantic Schemas
from pydantic import BaseModel, Field, field_validator
from typing import Optional
from datetime import datetime


class ServiceReviewBase(BaseModel):
    """Base schema for ServiceReview"""
    rating: int = Field(..., ge=1, le=5, description="Rating from 1 to 5 stars")
    review: Optional[str] = Field(None, max_length=1000, description="Review text (optional)")
    images: Optional[list[str]] = Field(None, max_length=5, description="List of image URLs (max 5)")
    
    @field_validator('rating')
    def validate_rating(cls, v: int) -> int:
        """Validate rating is between 1 and 5"""
        if v < 1 or v > 5:
            raise ValueError("Rating must be between 1 and 5")
        return v
    
    @field_validator('review')
    def validate_review(cls, v: Optional[str]) -> Optional[str]:
        """Validate and normalize review text"""
        if v is None:
            return v
        v = v.strip()
        if not v:
            return None
        if len(v) < 5:
            raise ValueError("Review must be at least 5 characters long")
        if len(v) > 1000:
            raise ValueError("Review cannot exceed 1000 characters")
        return v
    
    @field_validator('images')
    def validate_images(cls, v: Optional[list[str]]) -> Optional[list[str]]:
        """Validate image URLs"""
        if v is None:
            return v
        
        # Remove empty strings and duplicates
        v = list(dict.fromkeys([url.strip() for url in v if url and url.strip()]))
        
        if len(v) > 5:
            raise ValueError("Maximum 5 images allowed")
        
        # Basic URL validation
        for url in v:
            if not url.startswith(('http://', 'https://', '/')):
                raise ValueError(f"Invalid image URL: {url}")
            if len(url) > 500:
                raise ValueError(f"Image URL too long: {url}")
        
        return v if v else None


class ServiceReviewCreate(ServiceReviewBase):
    """Schema for creating a new service review"""
    service_id: int = Field(..., gt=0, description="Service ID reference")
    customer_id: str = Field(..., min_length=1, description="Customer ID reference")
    
    @field_validator('customer_id')
    def validate_customer_id(cls, v: str) -> str:
        """Validate customer ID"""
        v = v.strip()
        if not v:
            raise ValueError("Customer ID cannot be empty")
        return v


class ServiceReviewResponse(ServiceReviewBase):
    """Schema for service review response"""
    service_id: int = Field(..., description="Service ID reference")
    customer_id: str = Field(..., description="Customer ID reference")
    created_at: datetime = Field(..., description="Timestamp when review was created")
    
    class Config:
        from_attributes = True


class ServiceReviewUpdate(BaseModel):
    """Schema for updating a service review"""
    rating: Optional[int] = Field(None, ge=1, le=5, description="Updated rating")
    review: Optional[str] = Field(None, max_length=1000, description="Updated review text")
    images: Optional[list[str]] = Field(None, max_length=5, description="Updated list of image URLs")
    
    @field_validator('rating')
    def validate_rating(cls, v: Optional[int]) -> Optional[int]:
        """Validate rating is between 1 and 5"""
        if v is None:
            return v
        if v < 1 or v > 5:
            raise ValueError("Rating must be between 1 and 5")
        return v
    
    @field_validator('review')
    def validate_review(cls, v: Optional[str]) -> Optional[str]:
        """Validate and normalize review text"""
        if v is None:
            return v
        v = v.strip()
        if not v:
            raise ValueError("Review cannot be empty or only whitespace")
        if len(v) < 5:
            raise ValueError("Review must be at least 5 characters long")
        if len(v) > 1000:
            raise ValueError("Review cannot exceed 1000 characters")
        return v
    
    @field_validator('images')
    def validate_images(cls, v: Optional[list[str]]) -> Optional[list[str]]:
        """Validate image URLs"""
        if v is None:
            return v
        
        # Remove empty strings and duplicates
        v = list(dict.fromkeys([url.strip() for url in v if url and url.strip()]))
        
        if len(v) > 5:
            raise ValueError("Maximum 5 images allowed")
        
        # Basic URL validation
        for url in v:
            if not url.startswith(('http://', 'https://', '/')):
                raise ValueError(f"Invalid image URL: {url}")
            if len(url) > 500:
                raise ValueError(f"Image URL too long: {url}")
        
        return v if v else None


class ServiceReviewWithDetails(ServiceReviewResponse):
    """Schema for service review response with customer and service details"""
    customer: dict = Field(..., description="Customer details")
    service: dict = Field(..., description="Service details")
    
    class Config:
        from_attributes = True


class ServiceReviewStats(BaseModel):
    """Schema for service review statistics"""
    service_id: int = Field(..., description="Service ID")
    total_reviews: int = Field(..., ge=0, description="Total number of reviews")
    average_rating: float = Field(..., ge=0, le=5, description="Average rating")
    rating_distribution: dict[int, int] = Field(..., description="Distribution of ratings (1-5)")
    
    class Config:
        from_attributes = True


class ServiceReviewQuery(BaseModel):
    """Schema for querying service reviews"""
    service_id: Optional[int] = Field(None, gt=0, description="Filter by service ID")
    customer_id: Optional[str] = Field(None, min_length=1, description="Filter by customer ID")
    min_rating: Optional[int] = Field(None, ge=1, le=5, description="Minimum rating filter")
    max_rating: Optional[int] = Field(None, ge=1, le=5, description="Maximum rating filter")
    has_images: Optional[bool] = Field(None, description="Filter reviews with images")
    
    @field_validator('min_rating', 'max_rating')
    def validate_rating_range(cls, v: Optional[int]) -> Optional[int]:
        """Validate rating range"""
        if v is not None and (v < 1 or v > 5):
            raise ValueError("Rating must be between 1 and 5")
        return v