from sqlalchemy import Column, VARCHAR, TIMESTAMP
from sqlalchemy.sql import func
from app.database import Base

class RefreshToken(Base):
    """Access tokens for user authentication"""
    __tablename__ = "refresh_tokens"
    
    jti = Column(VARCHAR, primary_key=True)
    token = Column(VARCHAR, nullable=False)
    created_at = Column(TIMESTAMP, server_default=func.now())
    expires_at = Column(TIMESTAMP, nullable=False)
    
    def __repr__(self):
        return f"<RefreshToken(jti='{self.jti}')>"
    