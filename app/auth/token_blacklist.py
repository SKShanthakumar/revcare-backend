from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession as Session
from app.models import RevokedToken
from datetime import datetime

def add_to_blacklist(jti: str, expires_at: datetime, db: Session):
    """
    Add a token to the blacklist/revocation list.
    
    Creates a RevokedToken object with the JWT ID and expiration time,
    adds it to the database, and commits the change. This marks the token as revoked.
    
    Args:
        jti: Unique JWT identifier (JWT ID)
        expires_at: Token expiration datetime
        db: Database session
    """
    revoked = RevokedToken(jti=jti, expires_at=expires_at)
    db.add(revoked)
    db.commit()

async def is_token_blacklisted(jti: str, db: Session) -> bool:
    """
    Check if a token is blacklisted/revoked.
    
    Queries the RevokedToken table for the given jti. If a record exists:
    - If expired: removes from table and returns False (not blacklisted anymore)
    - If not expired: returns True (token is blacklisted)
    If no record exists, returns False (token is not blacklisted).
    
    Args:
        jti: Unique JWT identifier (JWT ID) to check
        db: Async database session
        
    Returns:
        bool: True if token is blacklisted, False otherwise
    """
    result = await db.execute(select(RevokedToken).where(RevokedToken.jti == jti))
    token = result.scalar_one_or_none()
    if token:
        # Optionally: remove expired tokens
        if token.expires_at < datetime.utcnow():
            db.delete(token)
            db.commit()
            return False
        return True
    return False

