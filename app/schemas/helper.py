from pydantic import BaseModel, Field, field_validator

class RewriteMessage(BaseModel):
    """Base schema for Area"""
    message: str = Field(..., min_length=1, description="Message to be rewritten")

    @field_validator('message')
    def validate_message(cls, v: str) -> str:
        """Validate and normalize message"""
        v = v.strip()
        if not v:
            raise ValueError("Message cannot be empty or only whitespace")
        if len(v.split()) < 2:
            raise ValueError("Message must be at least 2 words long")
        return v
