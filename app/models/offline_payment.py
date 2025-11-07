from sqlalchemy import Column, TIMESTAMP, ForeignKey, Integer, NUMERIC, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base

class OfflinePayment(Base):
    __tablename__ = "offline_payments"

    id = Column(Integer, primary_key=True, autoincrement=True)
    booking_id = Column(Integer, ForeignKey("bookings.id", ondelete="CASCADE"), nullable=False)
    status_id = Column(Integer, ForeignKey("status.id", ondelete="CASCADE"), nullable=False)
    amount = Column(NUMERIC(12, 2), nullable=False)
    gst = Column(NUMERIC(12, 2), nullable=False)
    paid_online = Column(Boolean, nullable=False, server_default="false")

    created_at = Column(TIMESTAMP, server_default=func.now())

    # Relationships
    booking = relationship("Booking", lazy="selectin")
    status = relationship("Status", lazy="selectin")

    def __repr__(self):
        return f"<OfflinePayment(id='{self.id}', booking_id='{self.booking_id}')>"
    