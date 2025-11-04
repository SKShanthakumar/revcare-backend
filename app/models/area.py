from sqlalchemy import Column, VARCHAR, Integer
from app.database import Base

class Area(Base):
    """Area data of the serving city"""
    __tablename__ = "areas"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(VARCHAR, nullable=False)
    pincode = Column(Integer, nullable=False)
    
    def __repr__(self):
        return f"<Area(id='{self.id}', name='{self.name}', pincode='{self.pincode}')>"
    