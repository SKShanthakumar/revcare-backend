from sqlalchemy import Column, Integer, VARCHAR, ForeignKey, BIGINT
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base

class User(Base):
    """All application users (customers, admins, mechanics)
    For common login search"""
    __tablename__ = "users"
    
    phone = Column(BIGINT, primary_key=True)
    password = Column(VARCHAR, nullable=False)
    role_id = Column(Integer, ForeignKey("roles.id", ondelete='CASCADE', onupdate='CASCADE'), nullable=False)
    
    # Relationships
    role = relationship("Role", back_populates="users")
    
    def __repr__(self):
        return f"<User(phone='{self.phone}', role_id='{self.role_id}')>"
