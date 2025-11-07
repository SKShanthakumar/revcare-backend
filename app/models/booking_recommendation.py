from sqlalchemy import Column, TIMESTAMP, ForeignKey, Integer, NUMERIC
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base

class BookingRecommendation(Base):
    """Mechanic recommendations for additional services"""
    __tablename__ = "booking_recommendations"
    
    booking_id = Column(Integer, ForeignKey("bookings.id", ondelete='CASCADE', onupdate='CASCADE'), primary_key=True)
    service_id = Column(Integer, ForeignKey("services.id", ondelete='CASCADE', onupdate='CASCADE'), primary_key=True)
    price = Column(NUMERIC(12, 2), nullable=False)
    created_at = Column(TIMESTAMP, server_default=func.now())
    
    # Relationships
    booking = relationship("Booking", back_populates="booking_recommendations")
    service = relationship("Service", lazy="selectin")
    
    def __repr__(self):
        return f"<BookingRecommendation(booking_id={self.booking_id}, service_id={self.service_id})>"
