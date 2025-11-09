from pydantic import BaseModel

class ContentUpdateResponse(BaseModel):
    content_id: str
    status: str
    