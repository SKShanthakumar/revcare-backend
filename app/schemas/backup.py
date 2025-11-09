"""
Pydantic schemas for Backup and Recovery endpoints
"""
from typing import Optional, Dict, List, Any
from pydantic import BaseModel, Field
from datetime import datetime


class PostgreSQLBackupInfo(BaseModel):
    """PostgreSQL backup information"""
    success: bool
    backup_name: str
    backup_path: str
    size_bytes: int
    size_mb: float
    created_at: str


class MongoDBBackupInfo(BaseModel):
    """MongoDB backup information"""
    success: bool
    backup_name: str
    backup_path: str
    collections: Dict[str, int]
    total_documents: int
    size_bytes: int
    size_mb: float
    created_at: str


class FullBackupInfo(BaseModel):
    """Full backup information for both databases"""
    success: bool
    timestamp: str
    postgresql: PostgreSQLBackupInfo
    mongodb: MongoDBBackupInfo
    total_size_mb: float


class BackupResponse(BaseModel):
    """Generic backup response"""
    success: bool
    # For full backup
    timestamp: Optional[str] = None
    postgresql: Optional[PostgreSQLBackupInfo] = None
    mongodb: Optional[MongoDBBackupInfo] = None
    total_size_mb: Optional[float] = None


class BackupItem(BaseModel):
    """Individual backup item in list"""
    name: str
    path: str
    size_mb: float
    created_at: str
    collections: Optional[Dict[str, int]] = None
    total_documents: Optional[int] = None


class BackupListResponse(BaseModel):
    """List of all available backups"""
    postgresql: List[BackupItem]
    mongodb: List[BackupItem]


class RestoreRequest(BaseModel):
    """Request body for restore operations"""
    backup_name: str = Field(..., description="Name of the backup to restore")
    drop_existing: Optional[bool] = Field(
        True, 
        description="Drop existing data before restore (MongoDB only)"
    )


class PostgreSQLRestoreInfo(BaseModel):
    """PostgreSQL restore result"""
    success: bool
    backup_name: str
    statements_executed: int
    restored_at: str


class MongoDBRestoreInfo(BaseModel):
    """MongoDB restore result"""
    success: bool
    backup_name: str
    collections_restored: Dict[str, int]
    total_documents: int
    restored_at: str


class FullRestoreInfo(BaseModel):
    """Full restore information"""
    success: bool
    postgresql: PostgreSQLRestoreInfo
    mongodb: MongoDBRestoreInfo
    restored_at: str


class RestoreResponse(BaseModel):
    """Generic restore response"""
    success: bool
    backup_name: Optional[str] = None
    restored_at: Optional[str] = None
    
    # For PostgreSQL
    statements_executed: Optional[int] = None
    
    # For MongoDB
    collections_restored: Optional[Dict[str, int]] = None
    total_documents: Optional[int] = None
    
    # For full restore
    postgresql: Optional[PostgreSQLRestoreInfo] = None
    mongodb: Optional[MongoDBRestoreInfo] = None


class DeleteBackupResponse(BaseModel):
    """Response for backup deletion"""
    success: bool
    backup_name: str
    deleted_at: str