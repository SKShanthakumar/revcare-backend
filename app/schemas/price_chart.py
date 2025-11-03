from pydantic import BaseModel, Field, field_validator
from datetime import datetime
from decimal import Decimal
from .car_class import CarClassResponse

class PriceChartCreateWithService(BaseModel):
    """Schema for creating a new price chart entry which would be added along with service"""
    car_class_id: int = Field(..., gt=0, description="Car class ID reference")
    price: Decimal = Field(..., ge=0, max_digits=12, decimal_places=2, description="Price for the service and car class")
    
    @field_validator('price')
    def validate_price(cls, v: Decimal) -> Decimal:
        """Validate price is non-negative and has proper precision"""
        if v < 0:
            raise ValueError("Price cannot be negative")
        
        # Ensure proper decimal places
        if v.as_tuple().exponent < -2:
            raise ValueError("Price can have at most 2 decimal places")
        
        # Ensure total digits don't exceed 12
        sign, digits, exponent = v.as_tuple()
        total_digits = len(digits)
        if total_digits > 12:
            raise ValueError("Price cannot exceed 12 digits in total")
        
        return v
    

class PriceChartResponseWithService(BaseModel):
    """Schema for price chart response with service and car class details"""
    car_class: CarClassResponse = Field(..., description="Car class details")
    price: Decimal = Field(..., ge=0, max_digits=12, decimal_places=2, description="Price for the service and car class")
    
    @field_validator('price')
    def validate_price(cls, v: Decimal) -> Decimal:
        """Validate price is non-negative and has proper precision"""
        if v < 0:
            raise ValueError("Price cannot be negative")
        
        # Ensure proper decimal places
        if v.as_tuple().exponent < -2:
            raise ValueError("Price can have at most 2 decimal places")
        
        # Ensure total digits don't exceed 12
        sign, digits, exponent = v.as_tuple()
        total_digits = len(digits)
        if total_digits > 12:
            raise ValueError("Price cannot exceed 12 digits in total")
        
        return v
    
    class Config:
        from_attributes = True
    