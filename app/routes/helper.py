from fastapi import APIRouter, Security
from fastapi.responses import JSONResponse
from app.auth.dependencies import validate_token
from app.services.llm import rewrite_message
from app.schemas import RewriteMessage

router = APIRouter()

# area routes
@router.post("/rewrite", response_class=JSONResponse)
async def rewrite(body: RewriteMessage, payload = Security(validate_token, scopes=[])):
    """
    Rewrite a sentence with LLM to fix gramatical and structural errors.
    
    Args:
        payload: Validated token payload
        
    Returns:
        JSONResponse: Rewritten message
    """
    return await rewrite_message(body.message)
