from sqlalchemy import Table, Column, Integer, VARCHAR, NUMERIC, SMALLINT, TIMESTAMP, CheckConstraint, ForeignKey, ARRAY, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base

service_fuel_types = Table(
    "service_fuel_types",
    Base.metadata,
    Column("service_id", Integer, ForeignKey("services.id", ondelete='CASCADE', onupdate='CASCADE')),
    Column("fuel_type_id", Integer, ForeignKey("fuel_types.id", ondelete='CASCADE', onupdate='CASCADE'))
)

class Service(Base):
    """Individual services"""
    __tablename__ = "services"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(VARCHAR, nullable=False)
    description = Column(Text, nullable=False)
    category_id = Column(Integer, ForeignKey("service_categories.id", ondelete='CASCADE', onupdate='CASCADE'), nullable=False)
    works = Column(ARRAY(VARCHAR), nullable=False)  # PostgreSQL array of strings
    warranty_kms = Column(Integer, CheckConstraint('warranty_kms >= 0'), nullable=False)
    warranty_months = Column(Integer, CheckConstraint('warranty_months >= 0'), nullable=False)
    time_hrs = Column(NUMERIC(5, 2), nullable=False)  # Up to 999.99 hours
    difficulty = Column(SMALLINT, CheckConstraint('difficulty BETWEEN 1 AND 5'), nullable=False)
    created_at = Column(TIMESTAMP, server_default=func.now())
    
    # Relationship
    category = relationship("ServiceCategory", back_populates="services", lazy="selectin")
    price_chart = relationship("PriceChart", back_populates="service", cascade="all, delete-orphan", lazy="selectin")
    reviews = relationship("ServiceReview", back_populates="service", cascade="all, delete-orphan", lazy="selectin")
    fuel_types = relationship("FuelType", secondary=service_fuel_types, lazy="selectin")
    
    def __repr__(self):
        return f"<Service(id={self.id}, title='{self.title}', category_id={self.category_id})>"