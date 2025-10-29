from pydantic import BaseModel, EmailStr, Field, field_validator
from typing import Optional
from datetime import date
import re

class MechanicBase(BaseModel):
    name: str = Field(..., min_length=1)
    phone: int = Field(..., ge=6000000000)
    dob: date
    pickup_drop: bool
    analysis: bool

    @field_validator("dob")
    def validate_dob(cls, value: date) -> date:
        today = date.today()
        age = today.year - value.year - ((today.month, today.day) < (value.month, value.day))
        
        if value > today:
            raise ValueError("Date of birth cannot be in the future.")
        if age < 18:
            raise ValueError("Mechanic must be at least 18 years old.")
        if age > 60:
            raise ValueError("Age cannot exceed 60 years.")
        
        return value

class MechanicCreate(MechanicBase):
    password: str = Field(
        ..., 
        min_length=8, 
        description="Must contain at least one uppercase, one lowercase, and one special character"
    )

    @field_validator("password")
    def validate_password(cls, v: str) -> str:
        if not re.search(r"[A-Z]", v):
            raise ValueError("Password must contain at least one uppercase letter")
        if not re.search(r"[a-z]", v):
            raise ValueError("Password must contain at least one lowercase letter")
        if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", v):
            raise ValueError("Password must contain at least one special character")
        return v

class MechanicResponse(MechanicBase):
    id: str
    assigned: Optional[bool] = False

    class Config:
        orm_mode = True

class MechanicUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1)
    email: Optional[EmailStr] = None
    pickup_drop: Optional[bool] = None
    analysis: Optional[bool] = None
    dob: Optional[date] = None
