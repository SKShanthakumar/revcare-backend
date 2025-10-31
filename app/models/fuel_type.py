from sqlalchemy import Column, VARCHAR, Integer
from app.database import Base

class FuelType(Base):
    """Car fuel type data"""
    __tablename__ = "fuel_types"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    fuel_name = Column(VARCHAR, nullable=False)
    
    def __repr__(self):
        return f"<FuelType(id='{self.id}', name='{self.name}')>"
    