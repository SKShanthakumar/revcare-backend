from sqlalchemy import Column, VARCHAR, ForeignKey, Integer, TIMESTAMP
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base

class Address(Base):
    """Customer addresses for pickup/drop"""
    __tablename__ = "addresses"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    customer_id = Column(VARCHAR, ForeignKey("customers.id", ondelete='CASCADE', onupdate='CASCADE'), nullable=False)
    label = Column(VARCHAR)
    line1 = Column(VARCHAR, nullable=False)
    line2 = Column(VARCHAR)
    area_id = Column(Integer, ForeignKey("areas.id", ondelete='CASCADE', onupdate='CASCADE'), nullable=False)
    created_at = Column(TIMESTAMP, server_default=func.now())
    
    # Relationships
    area = relationship("Area", lazy="selectin")
    customer = relationship("Customer", back_populates="addresses", lazy="selectin")
    
    def __repr__(self):
        return f"<Address(id={self.id}, label='{self.label}', customer_id='{self.customer_id}')>"
