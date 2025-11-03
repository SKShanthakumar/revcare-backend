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
    

class PriceChartBase(PriceChartCreateWithService):
    """Base schema for PriceChart"""
    service_id: int = Field(..., gt=0, description="Service ID reference")


class PriceChartCreate(PriceChartBase):
    """Schema for creating a new price chart entry"""
    pass


class PriceChartResponse(PriceChartBase):
    """Schema for price chart response"""
    created_at: datetime = Field(..., description="Timestamp when price chart entry was created")
    
    class Config:
        from_attributes = True


class PriceChartUpdate(BaseModel):
    """Schema for updating a price chart entry"""
    price: Decimal = Field(..., ge=0, max_digits=12, decimal_places=2, description="Updated price")
    
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


class PriceChartWithDetails(PriceChartResponse):
    """Schema for price chart response with service and car class details"""
    service: dict = Field(..., description="Service details")
    car_class: dict = Field(..., description="Car class details")
    
    class Config:
        from_attributes = True


class PriceChartBulkCreate(BaseModel):
    """Schema for bulk creating price chart entries"""
    entries: list[PriceChartCreate] = Field(..., min_length=1, description="List of price chart entries to create")
    
    @field_validator('entries')
    def validate_unique_combinations(cls, v: list[PriceChartCreate]) -> list[PriceChartCreate]:
        """Validate that service_id and car_class_id combinations are unique"""
        seen = set()
        for entry in v:
            combination = (entry.service_id, entry.car_class_id)
            if combination in seen:
                raise ValueError(f"Duplicate entry found for service_id={entry.service_id} and car_class_id={entry.car_class_id}")
            seen.add(combination)
        return v


class PriceQuery(BaseModel):
    """Schema for querying price"""
    service_id: int = Field(..., gt=0, description="Service ID")
    car_class_id: int = Field(..., gt=0, description="Car class ID")

    