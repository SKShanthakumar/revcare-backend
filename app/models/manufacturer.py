from sqlalchemy import Column, VARCHAR, Integer
from app.database import Base

class Manufacturer(Base):
    """Car manufacturers data"""
    __tablename__ = "manufacturers"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(VARCHAR, nullable=False)
    
    def __repr__(self):
        return f"<Manufacturer(id='{self.id}', name='{self.name}')>"
    