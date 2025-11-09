import uuid
from jose import JWTError, jwt
from datetime import datetime, timedelta
from app.core.config import settings

SECRET_KEY = settings.secret_key
REFRESH_SECRET_KEY = settings.refresh_secret_key
ALGORITHM = settings.hash_algorithm
ACCESS_TOKEN_EXPIRE_MINUTES = settings.access_token_expire_minutes
REFRESH_TOKEN_EXPIRE_DAYS = settings.refresh_token_expire_days

def create_access_token(data: dict):
    """
    Create a JWT access token with expiration and unique identifier.
    
    This function:
    1. Copies the payload (data) to avoid mutating the original
    2. Calculates expiration (exp) → current UTC + configured minutes
    3. Generates jti → unique token ID using UUID4
    4. Adds fields to payload: exp, type="access", jti, iat
    5. Encodes JWT with SECRET_KEY & configured algorithm
    
    Args:
        data: Dictionary containing token payload (typically user_id and role)
        
    Returns:
        str: JWT access token string
    """
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    jti = str(uuid.uuid4())
    to_encode.update({"exp": expire, "type": "access", "jti": jti, "iat": datetime.utcnow()})
    token = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return token
def create_refresh_token(data: dict):
    """
    Create a JWT refresh token with longer expiration.
    
    Similar to access token but with:
    - Longer expiration (configured days from .env)
    - Stored separately with REFRESH_SECRET_KEY
    - type = "refresh"
    - Returns jti and expire for potential revocation tracking
    
    Args:
        data: Dictionary containing token payload (typically user_id and role)
        
    Returns:
        tuple: (token, jti, expire) where:
            - token: JWT refresh token string
            - jti: Unique token identifier for revocation tracking
            - expire: Expiration datetime
    """
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
    jti = str(uuid.uuid4())
    to_encode.update({"exp": expire, "type": "refresh", "jti": jti, "iat": datetime.utcnow()})
    token = jwt.encode(to_encode, REFRESH_SECRET_KEY, algorithm=ALGORITHM)
    return token, jti, expire

def decode_access_token(token: str) -> dict | None:
    """
    Decode and verify a JWT access token.
    
    Decodes JWT using the access secret key and verifies that type is "access"
    to ensure a refresh token is not used by mistake.
    
    Args:
        token: JWT access token string to decode
        
    Returns:
        dict | None: Decoded token payload if valid, None if invalid or wrong type
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        if payload.get("type") != "access":
            return None
        return payload
    except JWTError:
        import traceback
        # traceback.print_exc()
        return None

def decode_refresh_token(token: str) -> dict | None:
    """
    Decode and verify a JWT refresh token.
    
    Same logic as decode_access_token but for refresh tokens.
    Only refresh tokens will pass the type check.
    
    Args:
        token: JWT refresh token string to decode
        
    Returns:
        dict | None: Decoded token payload if valid, None if invalid or wrong type
    """
    try:
        payload = jwt.decode(token, REFRESH_SECRET_KEY, algorithms=[ALGORITHM])
        if payload.get("type") != "refresh":
            return None
        return payload
    except JWTError:
        return None

