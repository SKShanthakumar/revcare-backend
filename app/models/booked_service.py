from sqlalchemy import Column, TIMESTAMP, ForeignKey, Integer, NUMERIC, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base

class BookedService(Base):
    """Services attached to a booking"""
    __tablename__ = "booked_services"
    
    booking_id = Column(Integer, ForeignKey("bookings.id", ondelete='CASCADE', onupdate='CASCADE'), primary_key=True)
    service_id = Column(Integer, ForeignKey("services.id", ondelete='CASCADE', onupdate='CASCADE'), primary_key=True)
    status_id = Column(Integer, ForeignKey("status.id", ondelete='CASCADE', onupdate='CASCADE'), nullable=False)
    est_price = Column(NUMERIC(12, 2), nullable=False)
    price = Column(NUMERIC(12, 2))
    completed = Column(Boolean, default=False, nullable=False)
    created_at = Column(TIMESTAMP, server_default=func.now())
    
    # Relationships
    booking = relationship("Booking", back_populates="booked_services")
    service = relationship("Service", lazy="selectin")
    status = relationship("Status", lazy="selectin")
    
    def __repr__(self):
        return f"<BookedService(booking_id={self.booking_id}, service_id={self.service_id})>"
