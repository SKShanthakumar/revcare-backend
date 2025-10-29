from sqlalchemy import Column, VARCHAR, TIMESTAMP, Boolean, ForeignKey, Date, FetchedValue
from sqlalchemy.sql import func
from app.database import Base

class Mechanic(Base):
    """Mechanic-specific attributes linked to users"""
    __tablename__ = "mechanics"
    
    id = Column(VARCHAR, primary_key=True, server_default=FetchedValue())
    name = Column(VARCHAR, nullable=False)
    phone = Column(VARCHAR, ForeignKey('users.phone'), unique=True, nullable=False, index=True)
    dob = Column(Date, nullable=False)
    pickup_drop = Column(Boolean, default=False)
    analysis = Column(Boolean, default=False)
    assigned = Column(Boolean, default=False)
    created_at = Column(TIMESTAMP, server_default=func.now())
    updated_at = Column(TIMESTAMP, onupdate=func.now())

    def __repr__(self):
        return f"<Mechanic(id={self.id}, name={self.name})>"