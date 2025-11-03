from sqlalchemy import Column, Integer, TIMESTAMP, ForeignKey, SMALLINT, VARCHAR, ARRAY
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base

class ServiceReview(Base):
    """Reviews added by customers to a service"""
    __tablename__ = "service_reviews"
    
    service_id = Column(Integer, ForeignKey("services.id", ondelete='CASCADE', onupdate='CASCADE'), primary_key=True)
    customer_id = Column(VARCHAR, ForeignKey("customers.id", ondelete='CASCADE', onupdate='CASCADE'), primary_key=True)
    rating = Column(SMALLINT, nullable=False)
    review = Column(VARCHAR)
    images = Column(ARRAY(VARCHAR))
    created_at = Column(TIMESTAMP, server_default=func.now())
    
    # Relationships
    customer = relationship("Customer", lazy="selectin")
    service = relationship("Service", back_populates="reviews", lazy="selectin")
    
    def __repr__(self):
        return f"<ServiceReview(service_id={self.service_id}, customer_id={self.customer_id}, price={self.price})>"
    