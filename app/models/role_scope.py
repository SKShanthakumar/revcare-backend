from sqlalchemy import Table, Column, Integer, VARCHAR, TIMESTAMP, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base

role_permissions = Table(
    "role_permissions",
    Base.metadata,
    Column("role_id", Integer, ForeignKey("roles.id", ondelete='CASCADE', onupdate='CASCADE')),
    Column("permission_id", Integer, ForeignKey("permissions.id", ondelete='CASCADE', onupdate='CASCADE'))
)

class Role(Base):
    """Role definitions"""
    __tablename__ = "roles"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    role_name = Column(VARCHAR, unique=True, nullable=False)
    created_at = Column(TIMESTAMP, server_default=func.now())

    # relationship
    permissions = relationship("Permission", secondary=role_permissions, back_populates="roles")
    users = relationship("User", back_populates="role", cascade='all')

    def __repr__(self):
        return f"<Role(id={self.id}, role_name='{self.role_name}')>"

class Permission(Base):
    """Individual permission labels used by roles"""
    __tablename__ = "permissions"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    permission = Column(VARCHAR, unique=True, nullable=False)
    
    # Many-to-Many relationship
    roles = relationship("Role", secondary=role_permissions, back_populates="permissions")
    
    def __repr__(self):
        return f"<Permission(id={self.id}, permission='{self.permission}')>"