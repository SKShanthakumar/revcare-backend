from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer, SecurityScopes
from sqlalchemy.orm import Session
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
def validate_token(security_scopes: SecurityScopes, token: str = Depends(oauth2_scheme), db: Session = Depends(get_postgres_db)):
    credentials_exception = HTTPException(
        status_code=401,
        detail="Could not validate credentials or insufficient permissions."
    )

    payload = decode_access_token(token)
    if payload is None:
        raise HTTPException(
            status_code=401,
            detail="Invalid token."
        )

    jti = payload.get("jti")
    if is_token_blacklisted(jti, db):
        raise HTTPException(status_code=403, detail="Token has been revoked.")
    
    user_id = payload.get("sub")
    user_type = user_id[:3]
    if user_type == 'CST':
        from app.models import Customer
        user = db.query(Customer).filter(Customer.id == user_id).first()
    elif user_type == 'MEC':
        from app.models import Mechanic
        user = db.query(Mechanic).filter(Mechanic.id == user_id).first()
    else:
        from app.models import Admin
        user = db.query(Admin).filter(Admin.id == user_id).first()
    
    if not user:
        raise credentials_exception

    role = payload.get("role")
    token_scopes = db.query(Role).filter(Role.id == role).first().permissions
    token_scopes = [p.permission for p in token_scopes]

    for scope in security_scopes.scopes:
        if scope not in token_scopes:
            raise credentials_exception
        
    response = {
        "user_id": user_id,
        "role": role,
        "user_data": user,
        "jti": jti,
        "exp": payload.get("exp") 
    }
        
    return response