from fastapi import APIRouter, Depends, Request, Response, HTTPException, Security, Form
from sqlalchemy.ext.asyncio import AsyncSession as Session
from app.database.dependencies import get_postgres_db
from app.schemas import Login
from app.core.config import settings
from app.services import auth
from app.auth.dependencies import validate_token

router = APIRouter()

REFRESH_TOKEN_EXPIRE_DAYS = settings.refresh_token_expire_days

@router.post("/login")
async def login(response: Response, username: str = Form(...), password: str = Form(...), db: Session = Depends(get_postgres_db)):
    """
    Authenticate user and generate access/refresh tokens.
    
    Validates user credentials (phone and password) and generates JWT tokens.
    Sets refresh token as HTTP-only cookie for security.
    
    Args:
        response: FastAPI Response object for setting cookies
        username: User's phone number (used as username)
        password: User's plain text password
        db: Database session
        
    Returns:
        dict: Dictionary containing access_token and token_type
        
    Raises:
        HTTPException: 401 if credentials are invalid
    """
    credentials = Login(phone=username, password=password)
    refresh_token, access_token = await auth.login_user(credentials, db)

    response.set_cookie(
        key="refresh_token",
        value=refresh_token,
        httponly=True,
        secure=False,
        samesite="lax",
        max_age=REFRESH_TOKEN_EXPIRE_DAYS*24*60*60
    )

    return {"access_token": access_token, "token_type": "bearer"}

@router.post("/refresh")
async def refresh_token(request: Request, db: Session = Depends(get_postgres_db)):
    """
    Refresh access token using refresh token from cookie.
    
    Validates the refresh token from HTTP-only cookie and generates a new access token.
    Used to obtain a new access token without re-authenticating.
    
    Args:
        request: FastAPI Request object to access cookies
        db: Database session
        
    Returns:
        JSONResponse: Contains new access_token and token_type
        
    Raises:
        HTTPException: 401 if refresh token is missing or invalid
    """
    refresh_token = request.cookies.get("refresh_token")
    if not refresh_token:
        raise HTTPException(status_code=401, detail="Refresh token missing")

    return await auth.get_access_token_using_refresh_token(refresh_token, db)

@router.post("/logout")
async def logout(request: Request, response: Response, payload = Security(validate_token, scopes=[]), db: Session = Depends(get_postgres_db)):
    """
    Logout user and revoke tokens.
    
    Blacklists both access and refresh tokens, removes refresh token from database,
    and deletes the refresh token cookie.
    
    Args:
        request: FastAPI Request object to access cookies
        response: FastAPI Response object for deleting cookies
        payload: Validated token payload from validate_token dependency
        db: Database session
        
    Returns:
        dict: Success message
    """
    refresh_token = request.cookies.get("refresh_token")
    await auth.logout_user(payload, refresh_token, db)

    # Delete refresh token cookie
    response.delete_cookie(key="refresh_token")

    return {"message": "Successfully logged out"}
