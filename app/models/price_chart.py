from sqlalchemy import Column, Integer, NUMERIC, TIMESTAMP, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base

class PriceChart(Base):
    """Pricing per service per car class"""
    __tablename__ = "price_chart"
    
    service_id = Column(Integer, ForeignKey("services.id", ondelete='CASCADE', onupdate='CASCADE'), primary_key=True)
    car_class_id = Column(Integer, ForeignKey("car_classes.id", ondelete='CASCADE', onupdate='CASCADE'), primary_key=True)
    price = Column(NUMERIC(12, 2), nullable=False)
    created_at = Column(TIMESTAMP, server_default=func.now())
    
    # Relationships
    car_class = relationship("CarClass", lazy="selectin")
    service = relationship("Service", back_populates="price_chart", lazy="selectin")
    
    def __repr__(self):
        return f"<PriceChart(service_id={self.service_id}, car_class_id={self.car_class_id}, price={self.price})>"
    