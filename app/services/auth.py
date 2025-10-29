from fastapi import HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from datetime import datetime, timezone
from app.models import User, Customer, Admin, Mechanic, RefreshToken, RevokedToken
from app.auth.hashing import verify_password
from app.auth.jwt_handler import create_access_token, create_refresh_token, decode_refresh_token
from app.auth.token_blacklist import is_token_blacklisted
from app.schemas import Login

def login_user(credentials: Login, db: Session):
    phone = credentials.phone
    password = credentials.password

    user = db.query(User).filter(User.phone == phone).first()
    if not user:
        raise HTTPException(status_code=401, detail="Invalid phone number.")
    
    if not verify_password(password, user.password):
        raise HTTPException(status_code=401, detail="Incorrect password.")
    
    role_id = user.role_id

    if user.role.role_name == 'customer':
        user = db.query(Customer).filter(Customer.phone == phone).first()
        user_id = user.id
    elif user.role.role_name == 'mechanic':
        user = db.query(Mechanic).filter(Mechanic.phone == phone).first()
        user_id = user.id
    else:
        user = db.query(Admin).filter(Admin.phone == phone).first()
        user_id = user.id

    access_token = create_access_token({"sub": user_id, "role": role_id})
    refresh_token, refresh_jti, refresh_expiry = create_refresh_token({"sub": user_id, "role": role_id})

    db_refresh_token = RefreshToken(
        jti = refresh_jti,
        token = refresh_token,
        user_id = user_id,
        expires_at = refresh_expiry
    )

    db.add(db_refresh_token)
    db.commit()

    return refresh_token, access_token

def get_access_token_using_refresh_token(refresh_token: str, db: Session):
    payload = decode_refresh_token(refresh_token)
    if not payload:
        raise HTTPException(status_code=401, detail="Invalid refresh token")

    user_id = payload.get("sub")
    user_role = payload.get("role")

    jti = payload.get("jti")
    print(jti)
    if is_token_blacklisted(jti, db):
        raise HTTPException(status_code=403, detail="Token has been revoked.")

    new_access_token = create_access_token({"sub": user_id, "role": user_role})

    return JSONResponse(content={"access_token": new_access_token, "token_type": "bearer"})

def logout_user(access_token_payload: str, db: Session):
    pass
    jti = access_token_payload.get("jti")
    exp_timestamp = access_token_payload.get("exp")
    exp = datetime.fromtimestamp(exp_timestamp, tz=timezone.utc)
    user_id = access_token_payload.get("sub")
    revoked_token = RevokedToken(jti=jti, expires_at=exp)
    db.add(revoked_token)

    refresh_token = db.query(RefreshToken).filter(RefreshToken.user_id == user_id).first()
    if refresh_token:
        print(refresh_token)
        refres_jti = refresh_token.jti
        refres_exp = refresh_token.expires_at

        revoked_token = RevokedToken(jti=refres_jti, expires_at=refres_exp)
        db.add(revoked_token)
        db.delete(refresh_token)

    db.commit()