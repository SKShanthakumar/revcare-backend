from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer, SecurityScopes
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession as Session
from app.database.dependencies import get_postgres_db
from app.models import Role, Permission
from .jwt_handler import decode_access_token
from .token_blacklist import is_token_blacklisted

# Define available scopes
oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/api/v1/auth/login",
    refreshUrl="/api/v1/auth/refresh", 
)

# Verify token + scopes
async def validate_token(security_scopes: SecurityScopes, token: str = Depends(oauth2_scheme), db: Session = Depends(get_postgres_db)):
    payload = decode_access_token(token)
    if payload is None:
        raise HTTPException(
            status_code=401,
            detail="Invalid token."
        )

    jti = payload.get("jti")
    if await is_token_blacklisted(jti, db):
        raise HTTPException(status_code=403, detail="Token has been revoked.")
    
    user_id = payload.get("sub")
    user_type = user_id[:3]
    if user_type == 'CST':
        from app.models import Customer
        user = await db.get(Customer, user_id)
    elif user_type == 'MEC':
        from app.models import Mechanic
        user = await db.get(Mechanic, user_id)
    else:
        from app.models import Admin
        user = await db.get(Admin, user_id)
    
    if not user:
        raise HTTPException(
            status_code=401,
            detail="Could not validate credentials."
        )

    role = payload.get("role")
    result = await db.execute(select(Role).options(selectinload(Role.permissions)).where(Role.id == role))
    role_obj = result.scalar_one_or_none()
    token_scopes = role_obj.permissions
    token_scopes = [p.permission for p in token_scopes]

    for scope in security_scopes.scopes:
        if scope not in token_scopes:
            raise HTTPException(
                status_code=401,
                detail="Insufficient permissions."
            )
        
    response = {
        "user_id": user_id,
        "role": role,
        "user_data": user,
        "jti": jti,
        "exp": payload.get("exp") 
    }
        
    return response