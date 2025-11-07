from sqlalchemy import Column, VARCHAR, TIMESTAMP, ForeignKey, Integer, Boolean, Text, ARRAY
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base

class BookingAnalysis(Base):
    """Final analysis record for a booking by mechanic"""
    __tablename__ = "booking_analysis"
    
    booking_id = Column(Integer, ForeignKey("bookings.id", ondelete='CASCADE', onupdate='CASCADE'), primary_key=True)
    mechanic_id = Column(VARCHAR, ForeignKey("mechanics.id", ondelete='CASCADE', onupdate='CASCADE'), nullable=False)
    description = Column(Text, nullable=False)
    recommendation = Column(Text, nullable=False)
    images = Column(ARRAY(VARCHAR), nullable=False)
    validated = Column(Boolean, default=False, nullable=False)
    created_at = Column(TIMESTAMP, server_default=func.now())
    
    # Relationships
    booking = relationship("Booking", back_populates="booking_analysis")
    mechanic = relationship("Mechanic", lazy="selectin")
    
    def __repr__(self):
        return f"<BookingAnalysis(booking_id={self.booking_id})>"
    