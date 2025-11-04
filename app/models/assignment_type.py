from sqlalchemy import Column, VARCHAR, Integer
from app.database import Base

class AssignmentType(Base):
    """Utility table to track type of service assignment to mechanic"""
    __tablename__ = "assignment_types"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(VARCHAR, nullable=False, unique=True)
    
    def __repr__(self):
        return f"<AssignmentType(id='{self.id}', name='{self.name}')>"
    