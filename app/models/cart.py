from sqlalchemy import Column, Integer, TIMESTAMP, ForeignKey, VARCHAR
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base

class Cart(Base):
    """services in customer cart"""
    __tablename__ = "cart"
    
    customer_id = Column(VARCHAR, ForeignKey("customers.id", ondelete='CASCADE', onupdate='CASCADE'), primary_key=True)
    service_id = Column(Integer, ForeignKey("services.id", ondelete='CASCADE', onupdate='CASCADE'), primary_key=True)
    created_at = Column(TIMESTAMP, server_default=func.now())
    
    # Relationships
    service = relationship("Service", lazy="selectin")
    
    def __repr__(self):
        return f"<Cart(service_id={self.service_id}, customer_id={self.customer_id})>"
    