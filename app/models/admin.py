from sqlalchemy import Column, VARCHAR, TIMESTAMP, ForeignKey, FetchedValue
from sqlalchemy.sql import func
from app.database import Base

class Admin(Base):
    """Admin specific data"""
    __tablename__ = "admins"
    
    id = Column(VARCHAR, primary_key=True, server_default=FetchedValue())
    name = Column(VARCHAR, nullable=False)
    phone = Column(VARCHAR, ForeignKey('users.phone'), unique=True, nullable=False, index=True)
    email = Column(VARCHAR, unique=True, nullable=False)
    profile_img = Column(VARCHAR)
    created_at = Column(TIMESTAMP, server_default=func.now())
    updated_at = Column(TIMESTAMP, onupdate=func.now())
    
    def __repr__(self):
        return f"<Admin(id='{self.id}', name='{self.name}', phone='{self.phone}')>"