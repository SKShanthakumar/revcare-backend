from sqlalchemy import Column, VARCHAR, TIMESTAMP, ForeignKey, FetchedValue, BIGINT, Integer
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base

class Customer(Base):
    """Customer specific data"""
    __tablename__ = "customers"
    
    id = Column(VARCHAR, primary_key=True, server_default=FetchedValue())
    name = Column(VARCHAR, nullable=False)
    phone = Column(BIGINT, ForeignKey('users.phone', ondelete='CASCADE', onupdate='CASCADE'), unique=True, nullable=False, index=True)
    email = Column(VARCHAR, unique=True, nullable=False)
    profile_img = Column(VARCHAR)
    role_id = Column(Integer, ForeignKey("roles.id", ondelete='CASCADE', onupdate='CASCADE'), nullable=False)
    created_at = Column(TIMESTAMP, server_default=func.now())
    updated_at = Column(TIMESTAMP, onupdate=func.now())
    
    # Relationships
    role = relationship("Role")
    
    def __repr__(self):
        return f"<Customer(id='{self.id}', name='{self.name}', phone='{self.phone}')>"
    