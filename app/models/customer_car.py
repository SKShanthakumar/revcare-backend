from sqlalchemy import Column, VARCHAR, TIMESTAMP, ForeignKey, Integer
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base

class CustomerCar(Base):
    """Cars added by customers"""
    __tablename__ = "customer_cars"
    
    reg_number = Column(VARCHAR, primary_key=True)
    car_id = Column(Integer, ForeignKey("cars.id", ondelete='CASCADE', onupdate='CASCADE'), nullable=False)
    customer_id = Column(VARCHAR, ForeignKey("customers.id", ondelete='CASCADE', onupdate='CASCADE'), nullable=False)
    created_at = Column(TIMESTAMP, server_default=func.now())

    # Relationships
    customer = relationship("Customer")
    car = relationship("Car")

    def __repr__(self):
        return f"<CustomerCar(reg='{self.reg_number}', car_id='{self.car_id}', customer_id='{self.customer_id}')>"
    
