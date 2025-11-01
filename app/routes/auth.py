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
    refresh_token = request.cookies.get("refresh_token")
    if not refresh_token:
        raise HTTPException(status_code=401, detail="Refresh token missing")

    return await auth.get_access_token_using_refresh_token(refresh_token, db)

@router.post("/logout")
async def logout(request: Request, response: Response, payload = Security(validate_token, scopes=[]), db: Session = Depends(get_postgres_db)):
    refresh_token = request.cookies.get("refresh_token")
    await auth.logout_user(payload, refresh_token, db)

    # Delete refresh token cookie
    response.delete_cookie(key="refresh_token")

    return {"message": "Successfully logged out"}
