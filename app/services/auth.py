from fastapi import HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession as Session
from datetime import datetime, timezone
from app.models import User, Customer, Admin, Mechanic, RefreshToken, RevokedToken
from app.auth.hashing import verify_password
from app.auth.jwt_handler import create_access_token, create_refresh_token, decode_refresh_token
from app.auth.token_blacklist import is_token_blacklisted
from app.schemas import Login

async def login_user(credentials: Login, db: Session):
    phone = credentials.phone
    password = credentials.password

    result = await db.execute(select(User).options(selectinload(User.role)).where(User.phone == phone))
    user = result.scalar_one_or_none()
    if not user:
        raise HTTPException(status_code=401, detail="Invalid phone number.")
    
    if not verify_password(password, user.password):
        raise HTTPException(status_code=401, detail="Incorrect password.")

    if user.role.role_name == 'customer':
        result = await db.execute(select(Customer).where(Customer.phone == phone))
    elif user.role.role_name == 'mechanic':
        result = await db.execute(select(Mechanic).where(Mechanic.phone == phone))
    else:
        result = await db.execute(select(Admin).where(Admin.phone == phone))
    user = result.scalar_one_or_none()

    access_token = create_access_token({"sub": user.id, "role": user.role_id})
    refresh_token, refresh_jti, refresh_expiry = create_refresh_token({"sub": user.id, "role": user.role_id})

    db_refresh_token = RefreshToken(
        jti = refresh_jti,
        token = refresh_token,
        user_id = user.id,
        expires_at = refresh_expiry
    )

    db.add(db_refresh_token)
    await db.commit()

    return refresh_token, access_token

async def get_access_token_using_refresh_token(refresh_token: str, db: Session):
    payload = decode_refresh_token(refresh_token)
    if not payload:
        raise HTTPException(status_code=401, detail="Invalid refresh token")

    user_id = payload.get("sub")
    user_role = payload.get("role")

    jti = payload.get("jti")
    
    if await is_token_blacklisted(jti, db):
        raise HTTPException(status_code=403, detail="Token has been revoked.")

    new_access_token = create_access_token({"sub": user_id, "role": user_role})

    return JSONResponse(content={"access_token": new_access_token, "token_type": "bearer"})

async def logout_user(access_token_payload: str, db: Session):
    jti = access_token_payload.get("jti")
    exp_timestamp = access_token_payload.get("exp")
    exp = datetime.fromtimestamp(exp_timestamp, tz=timezone.utc)
    user_id = access_token_payload.get("sub")

    # Blacklist access token
    revoked_token = RevokedToken(jti=jti, expires_at=exp)
    db.add(revoked_token)

    result = await db.execute(select(RefreshToken).where(RefreshToken.user_id == user_id))
    refresh_token = result.scalar_one_or_none()
    if refresh_token:
        refres_jti = refresh_token.jti
        refres_exp = refresh_token.expires_at

        # Blacklist refresh token
        revoked_token = RevokedToken(jti=refres_jti, expires_at=refres_exp)
        db.add(revoked_token)
        await db.delete(refresh_token)

    await db.commit()