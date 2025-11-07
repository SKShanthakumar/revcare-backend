from sqlalchemy import Column, VARCHAR, TIMESTAMP, ForeignKey, Integer
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base

class BookingAssignment(Base):
    """Assignment history of mechanics to bookings"""
    __tablename__ = "booking_assignment"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    mechanic_id = Column(VARCHAR, ForeignKey("mechanics.id", ondelete='CASCADE', onupdate='CASCADE'), nullable=False)
    booking_id = Column(Integer, ForeignKey("bookings.id", ondelete='CASCADE', onupdate='CASCADE'), nullable=False)
    assignment_type_id = Column(Integer, ForeignKey("assignment_types.id", ondelete='CASCADE', onupdate='CASCADE'), nullable=False)
    status_id = Column(Integer, ForeignKey("status.id", ondelete='CASCADE', onupdate='CASCADE'), nullable=False)
    assigned_at = Column(TIMESTAMP, server_default=func.now())
    
    # Relationships
    mechanic = relationship("Mechanic", lazy="selectin")
    booking = relationship("Booking", back_populates="booking_assignments")
    assignment_type = relationship("AssignmentType", lazy="selectin")
    status = relationship("Status", lazy="selectin")
    
    def __repr__(self):
        return f"<BookingAssignment(id={self.id}, booking_id={self.booking_id}, mechanic_id='{self.mechanic_id}')>"
