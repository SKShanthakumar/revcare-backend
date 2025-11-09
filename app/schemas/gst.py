from pydantic import BaseModel

class GstResponse(BaseModel):
    status: str
    updated_percent: int
    