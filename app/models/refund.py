from sqlalchemy import Column, TIMESTAMP, ForeignKey, Integer, NUMERIC, VARCHAR
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base

class Refund(Base):
    __tablename__ = "refunds"

    id = Column(Integer, primary_key=True, autoincrement=True)
    booking_id = Column(Integer, ForeignKey("bookings.id", ondelete="CASCADE"), nullable=False)
    customer_id = Column(VARCHAR, ForeignKey("customers.id", ondelete='CASCADE', onupdate='CASCADE'), nullable=False)
    status_id = Column(Integer, ForeignKey("status.id", ondelete="CASCADE"), nullable=False)
    amount = Column(NUMERIC(12, 2), nullable=False)
    created_at = Column(TIMESTAMP, server_default=func.now())

    # Relationships
    booking = relationship("Booking", lazy="selectin")
    status = relationship("Status", lazy="selectin")
    customer = relationship("Customer", lazy="selectin")

    def __repr__(self):
        return f"<Refund(id='{self.id}', booking_id='{self.booking_id}')>"
    