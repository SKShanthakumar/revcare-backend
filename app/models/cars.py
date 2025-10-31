from sqlalchemy import Column, VARCHAR, ForeignKey, Integer
from sqlalchemy.orm import relationship
from app.database import Base

class Car(Base):
    """Cars data"""
    __tablename__ = "cars"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    model = Column(VARCHAR, nullable=False)
    manufacturer_id = Column(Integer, ForeignKey("manufacturers.id", ondelete='CASCADE', onupdate='CASCADE'), nullable=False)
    fuel_type_id = Column(Integer, ForeignKey("fuel_types.id", ondelete='CASCADE', onupdate='CASCADE'), nullable=False)
    car_class_id = Column(Integer, ForeignKey("car_classes.id", ondelete='CASCADE', onupdate='CASCADE'), nullable=False)
    year = Column(Integer, nullable=False)
    img = Column(VARCHAR, nullable=False)
    
    # Relationships
    manufacturer = relationship("Manufacturer")
    fuel_type = relationship("FuelType")
    car_class = relationship("CarClass")
    
    def __repr__(self):
        return f"<Car(id='{self.id}', model='{self.model}')>"
    