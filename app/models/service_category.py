from sqlalchemy import Column, VARCHAR, Integer
from sqlalchemy.orm import relationship
from app.database import Base

class ServiceCategory(Base):
    """Service categories"""
    __tablename__ = "service_categories"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(VARCHAR, nullable=False, unique=True)
    description = Column(VARCHAR, nullable=False)

    # relationships
    services = relationship("Service", back_populates="category", lazy="selectin", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<ServiceCategory(id='{self.id}', name='{self.name}')>"
    