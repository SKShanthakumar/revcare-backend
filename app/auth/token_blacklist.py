from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession as Session
from app.models import RevokedToken
from datetime import datetime

def add_to_blacklist(jti: str, expires_at: datetime, db: Session):
    '''
    1.Create a RevokedToken object with:
        jti → unique JWT ID
        expires_at → token expiration time
    2.Add it to the database.
    3.Commit to save the change.
    This marks the token as revoked.
    '''
    revoked = RevokedToken(jti=jti, expires_at=expires_at)
    db.add(revoked)
    db.commit()

async def is_token_blacklisted(jti: str, db: Session) -> bool:
    '''
    1.Query RevokedToken table for the given jti.
    2.If a record exists:
        Check if it expired:
            Yes → remove from table and return False (not blacklisted anymore).
            No → return True (token is blacklisted).
    3. If no record → token is not blacklisted, return False.
    '''
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

