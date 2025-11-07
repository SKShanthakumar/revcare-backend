from sqlalchemy import Column, Integer, ForeignKey, TIMESTAMP, VARCHAR, ARRAY
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base

class ServiceSelectionStage(Base):
    __tablename__ = "service_selection_stage"
    id = Column(Integer, primary_key=True)
    booking_id = Column(Integer, ForeignKey("bookings.id"))
    razorpay_order_id = Column(VARCHAR(50), unique=True)
    selected_services = Column(ARRAY(Integer))
    created_at = Column(TIMESTAMP, server_default=func.now())

    # relationship
    booking = relationship("Booking", lazy="selectin")

    def __repr__(self):
        return f"<ServiceSelectionStage(booking_id={self.booking_id}>"
    