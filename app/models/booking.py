from sqlalchemy import Column, VARCHAR, TIMESTAMP, ForeignKey, Integer, Date
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base

class Booking(Base):
    """Booking header record"""
    __tablename__ = "bookings"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    customer_id = Column(VARCHAR, ForeignKey("customers.id", ondelete='CASCADE', onupdate='CASCADE'), nullable=False)
    car_reg_number = Column(VARCHAR, ForeignKey("customer_cars.reg_number", ondelete='CASCADE', onupdate='CASCADE'), nullable=False)
    status_id = Column(Integer, ForeignKey("status.id", ondelete='CASCADE', onupdate='CASCADE'), nullable=False)
    pickup_address_id = Column(Integer, ForeignKey("addresses.id", ondelete='CASCADE', onupdate='CASCADE'), nullable=False)
    pickup_date = Column(Date, nullable=False)
    pickup_timeslot_id = Column(Integer, ForeignKey("timeslots.id", ondelete='CASCADE', onupdate='CASCADE'), nullable=False)
    drop_address_id = Column(Integer, ForeignKey("addresses.id", ondelete='CASCADE', onupdate='CASCADE'), nullable=False)
    drop_date = Column(Date, nullable=False)
    drop_timeslot_id = Column(Integer, ForeignKey("timeslots.id", ondelete='CASCADE', onupdate='CASCADE'), nullable=False)
    created_at = Column(TIMESTAMP, server_default=func.now())
    completed_at = Column(TIMESTAMP)
    updated_at = Column(TIMESTAMP, onupdate=func.now())
    payment_method_id = Column(Integer, ForeignKey("payment_methods.id"), default=None)
    
    # Relationships
    customer = relationship("Customer", lazy="selectin")
    customer_car = relationship("CustomerCar", lazy="selectin")
    status = relationship("Status", lazy="selectin")
    pickup_address = relationship("Address", foreign_keys=[pickup_address_id], lazy="selectin")
    drop_address = relationship("Address", foreign_keys=[drop_address_id], lazy="selectin")
    pickup_timeslot = relationship("Timeslot", foreign_keys=[pickup_timeslot_id], lazy="selectin")
    drop_timeslot = relationship("Timeslot", foreign_keys=[drop_timeslot_id], lazy="selectin")
    booked_services = relationship("BookedService", back_populates="booking", lazy="selectin", cascade="all, delete-orphan")
    booking_recommendations = relationship("BookingRecommendation", back_populates="booking", lazy="selectin", cascade="all, delete-orphan")
    booking_assignments = relationship("BookingAssignment", back_populates="booking", lazy="selectin", cascade="all, delete-orphan")
    booking_progress = relationship("BookingProgress", back_populates="booking", lazy="selectin", cascade="all, delete-orphan")
    booking_analysis = relationship("BookingAnalysis", back_populates="booking", uselist=False, lazy="selectin", cascade="all, delete-orphan")
    payment_method = relationship("PaymentMethod", lazy="selectin")
    
    def __repr__(self):
        return f"<Booking(id={self.id}, customer_id='{self.customer_id}', status_id={self.status_id})>"
