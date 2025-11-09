from fastapi import APIRouter, Depends, HTTPException, Query, Security
from sqlalchemy.ext.asyncio import AsyncSession
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase
from app.auth.dependencies import validate_token
from app.database.dependencies import get_postgres_db, get_mongo_client, get_mongo_db
from app.services.backup import backup_service
from app.schemas.backup import (
    BackupResponse,
    BackupListResponse,
    RestoreResponse,
    DeleteBackupResponse
)

router = APIRouter()


@router.post("/create", response_model=BackupResponse)
async def create_full_backup(
    db: AsyncSession = Depends(get_postgres_db),
    mongo_client: AsyncIOMotorDatabase = Depends(get_mongo_db),
    payload = Security(validate_token, scopes=["WRITE:BACKUP"])
):
    """
    Create a backup of both PostgreSQL and MongoDB databases
    """
    return await backup_service.create_full_backup(db, mongo_client)


@router.get("/list", response_model=BackupListResponse)
async def list_backups(payload = Security(validate_token, scopes=["READ:BACKUP"])):
    """
    List all available backups for both databases
    """
    return backup_service.list_backups()


@router.post("/restore", response_model=RestoreResponse)
async def restore_full_backup(
    postgresql_backup: str = Query(..., description="PostgreSQL backup file name"),
    mongodb_backup: str = Query(..., description="MongoDB backup directory name"),
    db: AsyncSession = Depends(get_postgres_db),
    mongo_client: AsyncIOMotorClient = Depends(get_mongo_client),
    payload = Security(validate_token, scopes=["WRITE:BACKUP"])
):
    """
    Restore both databases from backups
    
    - **postgresql_backup**: Name of the PostgreSQL backup file
    - **mongodb_backup**: Name of the MongoDB backup directory
    
    Warning: This will delete all existing data in both databases
    """
    return await backup_service.restore_full_backup(
        db, 
        mongo_client, 
        postgresql_backup, 
        mongodb_backup
    )


@router.delete("/delete/{backup_name}", response_model=DeleteBackupResponse)
async def delete_backup(
    backup_name: str,
    backup_type: str = Query(..., description="Type of backup: 'postgresql' or 'mongodb'"),
    payload = Security(validate_token, scopes=["DELETE:BACKUP"])
):
    """
    Delete a backup file or directory
    
    - **backup_name**: Name of the backup to delete
    - **backup_type**: Type of backup ('postgresql' or 'mongodb')
    """
    if backup_type not in ['postgresql', 'mongodb']:
        raise HTTPException(
            status_code=400,
            detail="backup_type must be 'postgresql' or 'mongodb'"
        )
    
    return backup_service.delete_backup(backup_name, backup_type)
