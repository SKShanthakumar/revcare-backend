from sqlalchemy import Column, Integer, VARCHAR, TIMESTAMP, Boolean, ForeignKey, ARRAY, CheckConstraint
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base

class Permission(Base):
    """Individual permission labels used by roles"""
    __tablename__ = "permissions"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    permission = Column(VARCHAR, unique=True, nullable=False)
    
    def __repr__(self):
        return f"<Permission(id={self.id}, permission='{self.permission}')>"


class Role(Base):
    """Role definitions and link to permissions"""
    __tablename__ = "roles"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    role_name = Column(VARCHAR, unique=True, nullable=False)
    permissions = Column(ARRAY(Integer), nullable=False)
    created_at = Column(TIMESTAMP, server_default=func.now())
    
    # Relationships
    users = relationship("User", back_populates="role")
    
    def __repr__(self):
        return f"<Role(id={self.id}, role_name='{self.role_name}')>"


class User(Base):
    """All application users (customers, admins, mechanics)"""
    __tablename__ = "users"
    
    id = Column(VARCHAR, primary_key=True)
    name = Column(VARCHAR, nullable=False)
    phone = Column(VARCHAR, unique=True, nullable=False, index=True)
    email = Column(VARCHAR, unique=True, nullable=False, index=True)
    password = Column(VARCHAR, nullable=False)
    role_id = Column(Integer, ForeignKey("roles.id"), nullable=False)
    profile_img = Column(VARCHAR)
    created_at = Column(TIMESTAMP, server_default=func.now())
    updated_at = Column(TIMESTAMP, onupdate=func.now())
    
    # Relationships
    role = relationship("Role", back_populates="users")
    mechanic = relationship("Mechanic", back_populates="user", uselist=False)
    customer_cars = relationship("CustomerCar", back_populates="customer")
    cart_items = relationship("Cart", back_populates="customer")
    favourites = relationship("Favourite", back_populates="customer")
    addresses = relationship("Address", back_populates="customer")
    bookings = relationship("Booking", back_populates="customer")
    reviews = relationship("ServiceReview", back_populates="customer")
    notification_preference = relationship("NotificationPreference", back_populates="customer", uselist=False)
    notification_logs = relationship("NotificationLog", back_populates="customer")
    access_token = relationship("AccessToken", back_populates="user", uselist=False)
    backup_recovery_logs = relationship("BackupRecoveryLog", back_populates="admin")
    backup_schedules = relationship("BackupSchedule", back_populates="admin")
    
    def __repr__(self):
        return f"<User(id='{self.id}', name='{self.name}', email='{self.email}')>"


class Mechanic(Base):
    """Mechanic-specific attributes linked to users"""
    __tablename__ = "mechanics"
    
    id = Column(Integer, ForeignKey("users.id"), primary_key=True)
    service_categories = Column(ARRAY(Integer), nullable=False)
    pickup_drop = Column(Boolean, default=False)
    analysis = Column(Boolean, default=False)
    assigned = Column(Boolean, default=False)
    created_at = Column(TIMESTAMP, server_default=func.now())
    
    __table_args__ = (
        CheckConstraint("array_length(service_categories, 1) > 0", name="chk_mechanics_service_categories"),
    )
    
    # Relationships
    user = relationship("User", back_populates="mechanic")
    booking_assignments = relationship("BookingAssignment", back_populates="mechanic")
    booking_progress = relationship("BookingProgress", back_populates="mechanic")
    booking_analysis = relationship("BookingAnalysis", back_populates="mechanic")
    
    def __repr__(self):
        return f"<Mechanic(id={self.id}, assigned={self.assigned})>"


class AccessToken(Base):
    """Access tokens for user authentication"""
    __tablename__ = "access_tokens"
    
    user_id = Column(VARCHAR, ForeignKey("users.id"), primary_key=True)
    token = Column(VARCHAR, nullable=False)
    created_at = Column(TIMESTAMP, server_default=func.now())
    
    # Relationships
    user = relationship("User", back_populates="access_token")
    
    def __repr__(self):
        return f"<AccessToken(user_id='{self.user_id}')>"