from sqlalchemy import Column, VARCHAR, Integer
from app.database import Base

class Status(Base):
    """Utility table with all status data"""
    __tablename__ = "status"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(VARCHAR, nullable=False, unique=True)
    
    def __repr__(self):
        return f"<Status(id='{self.id}', name='{self.name}')>"
    