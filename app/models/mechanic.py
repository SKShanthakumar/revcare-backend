from sqlalchemy import Table, Column, VARCHAR, TIMESTAMP, Boolean, ForeignKey, Date, FetchedValue, BIGINT, Integer
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base

mechanic_service_categories = Table(
    "mechanic_service_categories",
    Base.metadata,
    Column("mechanic_id", VARCHAR, ForeignKey("mechanics.id", ondelete='CASCADE', onupdate='CASCADE')),
    Column("service_category_id", Integer, ForeignKey("service_categories.id", ondelete='CASCADE', onupdate='CASCADE'))
)

class Mechanic(Base):
    """Mechanic-specific attributes linked to users"""
    __tablename__ = "mechanics"
    
    id = Column(VARCHAR, primary_key=True, server_default=FetchedValue())
    name = Column(VARCHAR, nullable=False)
    phone = Column(BIGINT, ForeignKey('users.phone', ondelete='CASCADE', onupdate='CASCADE'), unique=True, nullable=False, index=True)
    dob = Column(Date, nullable=False)
    pickup_drop = Column(Boolean, default=False)
    analysis = Column(Boolean, default=False)
    assigned = Column(Boolean, default=False)
    role_id = Column(Integer, ForeignKey("roles.id", ondelete='CASCADE', onupdate='CASCADE'), nullable=False)
    created_at = Column(TIMESTAMP, server_default=func.now())
    updated_at = Column(TIMESTAMP, onupdate=func.now())
    
    # Relationships
    role = relationship("Role")
    service_categories = relationship("ServiceCategory", secondary=mechanic_service_categories, lazy="selectin")

    def __repr__(self):
        return f"<Mechanic(id={self.id}, name={self.name})>"