from fastapi import APIRouter, Depends, Request, Response, HTTPException, Security, Form
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from app.database.dependencies import get_postgres_db
from app.schemas import Login
from app.core.config import settings
from app.services import auth
from app.auth.dependencies import validate_token

router = APIRouter()

REFRESH_TOKEN_EXPIRE_DAYS = settings.refresh_token_expire_days

@router.post("/login")
def login(response: Response, username: str = Form(...), password: str = Form(...), db: Session = Depends(get_postgres_db)):
    credentials = Login(phone=username, password=password)
    refresh_token, access_token = auth.login_user(credentials, db)

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
def refresh_token(request: Request, response: Response, db: Session = Depends(get_postgres_db)):
    refresh_token = request.cookies.get("refresh_token")
    if not refresh_token:
        raise HTTPException(status_code=401, detail="Refresh token missing")

    return auth.get_access_token_using_refresh_token(refresh_token, db)

@router.post("/logout")
def logout(response: Response, payload = Security(validate_token, scopes=[]), db: Session = Depends(get_postgres_db)):
    auth.logout_user(payload, db)

    # Delete refresh token cookie
    response.delete_cookie(key="refresh_token")

    return JSONResponse(content={"message": "Successfully logged out"})
