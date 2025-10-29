from pydantic import BaseModel, EmailStr, Field, field_validator
from typing import Optional
import re

class CustomerBase(BaseModel):
    name: str = Field(..., min_length=1)
    phone: int = Field(..., ge=6000000000)
    email: EmailStr

class CustomerCreate(CustomerBase):
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

class CustomerResponse(CustomerBase):
    id: str

    class Config:
        orm_mode = True

class CustomerUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1)
    email: Optional[EmailStr] = None