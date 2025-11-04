"""
SQLAlchemy Models for Vehicle Service Management System
"""

from app.database import Base, engine

# User related models
from .admin import *
from .customer import *
from .mechanic import *
from .user import *
from .role_scope import *
from .refresh_token import *
from .revoked_token import *
from .car_class import *
from .car import *
from .customer_car import *
from .fuel_type import *
from .manufacturer import *
from .area import *
from .address import *
from .price_chart import *
from .service import *
from .service_category import *
from .service_reviews import *
from .cart import *
from .favourite import *
from .assignment_type import *
from .timeslot import *
from .status import *
