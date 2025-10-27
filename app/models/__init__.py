"""
SQLAlchemy Models for Vehicle Service Management System
"""

from app.database import Base, engine

# User related models
from user_models import User, Role, Permission, Mechanic, AccessToken
