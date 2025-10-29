from pydantic import BaseModel, Field

class Login(BaseModel):
    phone: int = Field(..., ge=6000000000)
    password: str = Field(
        ..., 
        min_length=8, 
        description="Must contain at least one uppercase, one lowercase, and one special character"
    )
