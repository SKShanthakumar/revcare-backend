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
    '''
    1. Copy the payload (data) to avoid mutating the original.
    2. Calculate expiration (exp) → current UTC + 15 minutes.
    3. Generate jti → unique token ID using UUID4.
    4. Add fields to payload:
        exp → expiration
        type → "access" (to differentiate from refresh tokens)
        jti → unique token identifier
    5. Encode JWT with SECRET_KEY & HS256 algorithm
    6.Return:
        token → JWT string
        jti → store in DB if implementing revocation
        expire → optional, for DB record
    '''
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    jti = str(uuid.uuid4())
    to_encode.update({"exp": expire, "type": "access", "jti": jti, "iat": datetime.utcnow()})
    token = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return token
# Create Refresh Token

def create_refresh_token(data: dict):
    '''
    Same as access token but:Longer expiration (7 days or days mentioned in .env).
    Stored separately with REFRESH_SECRET_KEY.
    type = "refresh"
    You can store this jti in revoked_tokens table for refresh token revocation if needed.
    '''
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
    jti = str(uuid.uuid4())
    to_encode.update({"exp": expire, "type": "refresh", "jti": jti, "iat": datetime.utcnow()})
    token = jwt.encode(to_encode, REFRESH_SECRET_KEY, algorithm=ALGORITHM)
    return token, jti, expire

# Decode / Verify Access Token
'''
Decode JWT using the access secret key.
Check that type is "access" → ensures a refresh token is not used by mistake.
Returns payload if valid, else None.'''

def decode_access_token(token: str) -> dict | None:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        if payload.get("type") != "access":
            return None
        return payload
    except JWTError:
        return None

# Decode/Verify Refresh token
'''
Same logic but for refresh tokens.
Only refresh tokens will pass the type check.'''

def decode_refresh_token(token: str) -> dict | None:
    try:
        payload = jwt.decode(token, REFRESH_SECRET_KEY, algorithms=[ALGORITHM])
        if payload.get("type") != "refresh":
            return None
        return payload
    except JWTError:
        return None

