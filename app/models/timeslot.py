from sqlalchemy import Column, VARCHAR, Integer, TIME
from app.database import Base

class Timeslot(Base):
    """Utility table to store timeslot data for pickup and drop"""
    __tablename__ = "timeslots"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(VARCHAR, nullable=False, unique=True)
    start_time = Column(TIME, nullable=False)
    end_time = Column(TIME, nullable=False)
    
    def __repr__(self):
        return f"<Timeslot(id='{self.id}', name='{self.name}')>"
    