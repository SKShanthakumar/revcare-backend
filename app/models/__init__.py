"""
SQLAlchemy Models for Vehicle Service Management System
"""

from app.database import Base, engine

# User related models
from .admin import Admin
from .customer import Customer
from .mechanic import Mechanic
from .user import User
from .role_scope import Role, Permission
from .refresh_token import RefreshToken