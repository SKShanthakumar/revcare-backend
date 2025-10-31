from sqlalchemy import Column, VARCHAR, Integer
from app.database import Base

class CarClass(Base):
    """Car class data - to categorize cars"""
    __tablename__ = "car_classes"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    class_ = Column("class", VARCHAR, nullable=False)
    
    def __repr__(self):
        return f"<CarClass(id='{self.id}', class='{self.class_}')>"
    