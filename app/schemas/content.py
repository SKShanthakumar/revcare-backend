from pydantic import BaseModel
from pydantic import Field

class ContentBase(BaseModel):
    content_id: str = Field(..., description="Unique content identifier")

class ContentUpdateResponse(ContentBase):
    status: str
    
class ContentResposne(ContentBase):
    data: str = Field(..., description="Content data or image URL")
    