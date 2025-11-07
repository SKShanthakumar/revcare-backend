from sqlalchemy import Column, VARCHAR, TIMESTAMP, ForeignKey, Integer, Boolean, Text, ARRAY
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base

class BookingProgress(Base):
    """Mechanic progress updates during service"""
    __tablename__ = "booking_progress"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    mechanic_id = Column(VARCHAR, ForeignKey("mechanics.id", ondelete='CASCADE', onupdate='CASCADE'), nullable=False)
    booking_id = Column(Integer, ForeignKey("bookings.id", ondelete='CASCADE', onupdate='CASCADE'), nullable=False)
    description = Column(Text, nullable=False)
    images = Column(ARRAY(VARCHAR), nullable=False)
    status_id = Column(Integer, ForeignKey("status.id", ondelete='CASCADE', onupdate='CASCADE'), nullable=False)
    validated = Column(Boolean, default=False, nullable=False)
    created_at = Column(TIMESTAMP, server_default=func.now())
    
    # Relationships
    mechanic = relationship("Mechanic", lazy="selectin")
    booking = relationship("Booking", back_populates="booking_progress")
    status = relationship("Status", lazy="selectin")
    
    def __repr__(self):
        return f"<BookingProgress(id={self.id}, booking_id={self.booking_id})>"
