# app/models/notification.py
from sqlalchemy import Column, VARCHAR, Integer, TIMESTAMP, ARRAY, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base

class NotificationCategory(Base):
    """Categories of notifications"""
    __tablename__ = "notification_categories"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(VARCHAR, nullable=False, unique=True)
    
    def __repr__(self):
        return f"<NotificationCategory(id={self.id}, name='{self.name}')>"


class NotificationLog(Base):
    """Log of notifications sent"""
    __tablename__ = "notification_log"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    notification_category_id = Column(Integer, ForeignKey("notification_categories.id", ondelete='CASCADE', onupdate='CASCADE'), nullable=False)
    recipient_email = Column(VARCHAR, nullable=False)
    subject = Column(VARCHAR, nullable=False)
    attachments = Column(ARRAY(VARCHAR), nullable=True)
    timestamp = Column(TIMESTAMP, server_default=func.now())
    
    # Relationships
    category = relationship("NotificationCategory", lazy="selectin")
    
    def __repr__(self):
        return f"<NotificationLog(id={self.id}, recipient='{self.recipient_email}')>"
