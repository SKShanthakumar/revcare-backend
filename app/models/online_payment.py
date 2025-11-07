from sqlalchemy import Column, TIMESTAMP, ForeignKey, Integer, NUMERIC, VARCHAR
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base

class OnlinePayment(Base):
    __tablename__ = "online_payments"

    id = Column(Integer, primary_key=True, autoincrement=True)
    booking_id = Column(Integer, ForeignKey("bookings.id", ondelete="CASCADE"), nullable=False)
    status_id = Column(Integer, ForeignKey("status.id", ondelete="CASCADE"), nullable=False)
    amount = Column(NUMERIC(12, 2), nullable=False)
    gst = Column(NUMERIC(12, 2), nullable=False)
    
    # Razorpay references
    razorpay_order_id = Column(VARCHAR(50), unique=True, nullable=False, index=True)
    razorpay_payment_id = Column(VARCHAR(50))
    razorpay_signature = Column(VARCHAR(100))

    created_at = Column(TIMESTAMP, server_default=func.now())

    # Relationships
    booking = relationship("Booking", lazy="selectin")
    status = relationship("Status", lazy="selectin")

    def __repr__(self):
        return f"<OnlinePayment(id='{self.id}', booking_id='{self.booking_id}')>"
    