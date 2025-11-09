import json
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Any, Optional
import shutil

from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase
from fastapi import HTTPException

from app.core.config import settings


class BackupService:
    """
    Service for handling database backups and recovery.
    
    Provides methods to create, restore, list, and delete backups for both
    PostgreSQL and MongoDB databases.
    """
    
    def __init__(self, backup_dir: str = "backups"):
        """
        Initialize BackupService with backup directory.
        
        Args:
            backup_dir: Directory path for storing backups (default: "backups")
        """
        self.backup_dir = Path(backup_dir)
        self.backup_dir.mkdir(exist_ok=True, parents=True)
        
    def _get_backup_path(self, backup_name: str) -> Path:
        """
        Get full path for a backup file or directory.
        
        Args:
            backup_name: Name of the backup file or directory
            
        Returns:
            Path: Full path to the backup
        """
        return self.backup_dir / backup_name
    
    async def create_postgresql_backup(
        self, 
        db_session: AsyncSession,
        backup_name: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Create PostgreSQL backup using SQLAlchemy.
        
        Exports all tables from the database as SQL INSERT statements.
        Creates a timestamped backup file if backup_name is not provided.
        
        Args:
            db_session: Async database session
            backup_name: Optional backup file name (default: auto-generated with timestamp)
            
        Returns:
            dict: Backup information including name, path, size, and creation time
            
        Raises:
            HTTPException: 500 if backup creation fails
        """
        if not backup_name:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_name = f"postgresql_backup_{timestamp}.sql"
        
        backup_path = self._get_backup_path(backup_name)
        
        try:
            # Get all table names
            result = await db_session.execute(
                text("""
                    SELECT tablename 
                    FROM pg_tables 
                    WHERE schemaname = 'public'
                """)
            )
            tables = [row[0] for row in result.fetchall()]
            
            with open(backup_path, 'w') as f:
                f.write("-- PostgreSQL Backup\n")
                f.write(f"-- Created at: {datetime.now().isoformat()}\n")
                f.write("-- ===================================\n\n")
                
                # Backup each table
                for table in tables:
                    f.write(f"\n-- Table: {table}\n")
                    f.write(f"DELETE FROM {table};\n")
                    
                    # Get column names
                    col_result = await db_session.execute(
                        text(f"""
                            SELECT column_name 
                            FROM information_schema.columns 
                            WHERE table_name = '{table}' 
                            ORDER BY ordinal_position
                        """)
                    )
                    columns = [row[0] for row in col_result.fetchall()]
                    
                    if not columns:
                        continue
                    
                    # Get data
                    data_result = await db_session.execute(
                        text(f"SELECT * FROM {table}")
                    )
                    rows = data_result.fetchall()
                    
                    if rows:
                        for row in rows:
                            values = []
                            for val in row:
                                if val is None:
                                    values.append('NULL')
                                elif isinstance(val, str):
                                    # Escape single quotes
                                    escaped = val.replace("'", "''")
                                    values.append(f"'{escaped}'")
                                elif isinstance(val, (int, float)):
                                    values.append(str(val))
                                elif isinstance(val, datetime):
                                    values.append(f"'{val.isoformat()}'")
                                else:
                                    values.append(f"'{str(val)}'")
                            
                            values_str = ', '.join(values)
                            columns_str = ', '.join(columns)
                            f.write(
                                f"INSERT INTO {table} ({columns_str}) "
                                f"VALUES ({values_str});\n"
                            )
            
            file_size = backup_path.stat().st_size
            
            return {
                "success": True,
                "backup_name": backup_name,
                "backup_path": str(backup_path),
                "size_bytes": file_size,
                "size_mb": round(file_size / (1024 * 1024), 2),
                "created_at": datetime.now().isoformat()
            }
            
        except Exception as e:
            if backup_path.exists():
                backup_path.unlink()
            raise HTTPException(
                status_code=500,
                detail=f"PostgreSQL backup failed: {str(e)}"
            )
    
    async def create_mongodb_backup(
        self,
        mongo_client: AsyncIOMotorClient,
        backup_name: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Create MongoDB backup by exporting collections to JSON.
        
        Exports all collections to JSON files and creates a metadata file.
        Creates a timestamped backup directory if backup_name is not provided.
        
        Args:
            mongo_client: MongoDB client or database instance
            backup_name: Optional backup directory name (default: auto-generated with timestamp)
            
        Returns:
            dict: Backup information including name, path, collections, document counts, size, and creation time
            
        Raises:
            HTTPException: 500 if backup creation fails
        """
        if not backup_name:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_name = f"mongodb_backup_{timestamp}"
        
        backup_path = self._get_backup_path(backup_name)
        backup_path.mkdir(exist_ok=True)
        
        try:
            # Get the database - mongo_client is already the database instance
            # If mongo_client is actually the client, use: db = mongo_client.get_database()
            # If mongo_client is the database, use it directly
            if hasattr(mongo_client, 'list_collection_names'):
                db = mongo_client  # It's already a database
            else:
                db = mongo_client.get_database()  # Get default database
            
            # Get all collection names
            collections = await db.list_collection_names()
            
            total_docs = 0
            collection_info = {}
            
            for collection_name in collections:
                collection = db[collection_name]
                
                # Get all documents
                cursor = collection.find({})
                documents = await cursor.to_list(length=None)
                
                # Convert ObjectId and datetime to string
                for doc in documents:
                    if '_id' in doc:
                        doc['_id'] = str(doc['_id'])
                    for key, value in doc.items():
                        if isinstance(value, datetime):
                            doc[key] = value.isoformat()
                
                # Save to JSON file
                collection_file = backup_path / f"{collection_name}.json"
                with open(collection_file, 'w') as f:
                    json.dump(documents, f, indent=2, default=str)
                
                collection_info[collection_name] = len(documents)
                total_docs += len(documents)
            
            # Create metadata file
            metadata = {
                "backup_name": backup_name,
                "created_at": datetime.now().isoformat(),
                "database": db.name,  # Get actual database name
                "collections": collection_info,
                "total_documents": total_docs
            }
            
            with open(backup_path / "metadata.json", 'w') as f:
                json.dump(metadata, f, indent=2)
            
            # Calculate total size
            total_size = sum(
                f.stat().st_size 
                for f in backup_path.rglob('*') 
                if f.is_file()
            )
            
            return {
                "success": True,
                "backup_name": backup_name,
                "backup_path": str(backup_path),
                "collections": collection_info,
                "total_documents": total_docs,
                "size_bytes": total_size,
                "size_mb": round(total_size / (1024 * 1024), 2),
                "created_at": datetime.now().isoformat()
            }
            
        except Exception as e:
            if backup_path.exists():
                shutil.rmtree(backup_path)
            raise HTTPException(
                status_code=500,
                detail=f"MongoDB backup failed: {str(e)}"
            )
    
    async def create_full_backup(
        self,
        db_session: AsyncSession,
        mongo_client: AsyncIOMotorDatabase
    ) -> Dict[str, Any]:
        """
        Create backup for both PostgreSQL and MongoDB databases.
        
        Creates backups for both databases with the same timestamp.
        
        Args:
            db_session: Async database session for PostgreSQL
            mongo_client: MongoDB client or database instance
            
        Returns:
            dict: Combined backup information for both databases
            
        Raises:
            HTTPException: 500 if backup creation fails for either database
        """
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # Create PostgreSQL backup
        pg_backup = await self.create_postgresql_backup(
            db_session,
            f"postgresql_backup_{timestamp}.sql"
        )
        
        # Create MongoDB backup
        mongo_backup = await self.create_mongodb_backup(
            mongo_client,
            f"mongodb_backup_{timestamp}"
        )
        
        return {
            "success": True,
            "timestamp": timestamp,
            "postgresql": pg_backup,
            "mongodb": mongo_backup,
            "total_size_mb": pg_backup["size_mb"] + mongo_backup["size_mb"]
        }
    
    def list_backups(self) -> Dict[str, List[Dict[str, Any]]]:
        """
        List all available backups for both databases.
        
        Scans the backup directory and returns lists of PostgreSQL and MongoDB backups
        with metadata including name, path, size, and creation time.
        
        Returns:
            dict: Dictionary with 'postgresql' and 'mongodb' keys containing lists of backup info
        """
        postgresql_backups = []
        mongodb_backups = []
        
        for item in self.backup_dir.iterdir():
            if item.is_file() and item.suffix == '.sql':
                postgresql_backups.append({
                    "name": item.name,
                    "path": str(item),
                    "size_mb": round(item.stat().st_size / (1024 * 1024), 2),
                    "created_at": datetime.fromtimestamp(
                        item.stat().st_ctime
                    ).isoformat()
                })
            elif item.is_dir() and 'mongodb_backup' in item.name:
                metadata_file = item / "metadata.json"
                if metadata_file.exists():
                    with open(metadata_file, 'r') as f:
                        metadata = json.load(f)
                    
                    total_size = sum(
                        f.stat().st_size 
                        for f in item.rglob('*') 
                        if f.is_file()
                    )
                    
                    mongodb_backups.append({
                        "name": item.name,
                        "path": str(item),
                        "size_mb": round(total_size / (1024 * 1024), 2),
                        "collections": metadata.get("collections", {}),
                        "total_documents": metadata.get("total_documents", 0),
                        "created_at": metadata.get("created_at")
                    })
        
        return {
            "postgresql": sorted(
                postgresql_backups, 
                key=lambda x: x["created_at"], 
                reverse=True
            ),
            "mongodb": sorted(
                mongodb_backups, 
                key=lambda x: x["created_at"], 
                reverse=True
            )
        }
    
    async def restore_postgresql_backup(
        self,
        db_session: AsyncSession,
        backup_name: str
    ) -> Dict[str, Any]:
        """
        Restore PostgreSQL database from backup.
        
        Restores database by executing SQL statements from the backup file.
        WARNING: This will delete all existing data in the database.
        
        Args:
            db_session: Async database session
            backup_name: Name of the backup file to restore from
            
        Returns:
            dict: Restore information including backup name and statements executed
            
        Raises:
            HTTPException: 
                - 404 if backup file is not found
                - 500 if restore fails
        """
        backup_path = self._get_backup_path(backup_name)
        
        if not backup_path.exists():
            raise HTTPException(
                status_code=404,
                detail=f"Backup file not found: {backup_name}"
            )
        
        try:
            with open(backup_path, 'r') as f:
                sql_content = f.read()
            
            # Split by statement and execute
            statements = [
                stmt.strip() 
                for stmt in sql_content.split(';') 
                if stmt.strip() and not stmt.strip().startswith('--')
            ]
            
            executed = 0
            for statement in statements:
                if statement:
                    try:
                        await db_session.execute(text(statement))
                    except Exception as e:
                        if 'UndefinedColumn' in str(e):
                            continue
                        
                    executed += 1
            
            await db_session.commit()
            
            return {
                "success": True,
                "backup_name": backup_name,
                "statements_executed": executed,
                "restored_at": datetime.now().isoformat()
            }
            
        except Exception as e:
            await db_session.rollback()
            raise HTTPException(
                status_code=500,
                detail=f"PostgreSQL restore failed: {str(e)}"
            )
    
    async def restore_mongodb_backup(
        self,
        mongo_client: AsyncIOMotorClient,
        backup_name: str,
        drop_existing: bool = True
    ) -> Dict[str, Any]:
        """
        Restore MongoDB database from backup.
        
        Restores collections from JSON files in the backup directory.
        WARNING: This will delete all existing data in collections if drop_existing is True.
        
        Args:
            mongo_client: MongoDB client or database instance
            backup_name: Name of the backup directory to restore from
            drop_existing: If True, drop existing collections before restoring (default: True)
            
        Returns:
            dict: Restore information including backup name, restored collections, and document counts
            
        Raises:
            HTTPException: 
                - 404 if backup directory is not found
                - 400 if backup is invalid (metadata.json not found)
                - 500 if restore fails
        """
        backup_path = self._get_backup_path(backup_name)
        
        if not backup_path.exists():
            raise HTTPException(
                status_code=404,
                detail=f"Backup directory not found: {backup_name}"
            )
        
        try:
            # Get the database - same logic as create_mongodb_backup
            if hasattr(mongo_client, 'list_collection_names'):
                db = mongo_client  # It's already a database
            else:
                db = mongo_client.get_database()  # Get default database
            
            # Read metadata
            metadata_file = backup_path / "metadata.json"
            if not metadata_file.exists():
                raise HTTPException(
                    status_code=400,
                    detail="Invalid backup: metadata.json not found"
                )
            
            with open(metadata_file, 'r') as f:
                metadata = json.load(f)
            
            restored_collections = {}
            
            for collection_name, doc_count in metadata["collections"].items():
                collection_file = backup_path / f"{collection_name}.json"
                
                if not collection_file.exists():
                    continue
                
                with open(collection_file, 'r') as f:
                    documents = json.load(f)
                
                collection = db[collection_name]
                
                # Drop existing collection if requested
                if drop_existing:
                    await collection.drop()
                
                # Insert documents
                if documents:
                    # Convert string _id back to ObjectId if needed
                    from bson import ObjectId
                    for doc in documents:
                        if '_id' in doc and isinstance(doc['_id'], str):
                            try:
                                doc['_id'] = ObjectId(doc['_id'])
                            except:
                                pass
                    
                    await collection.insert_many(documents)
                
                restored_collections[collection_name] = len(documents)
            
            return {
                "success": True,
                "backup_name": backup_name,
                "collections_restored": restored_collections,
                "total_documents": sum(restored_collections.values()),
                "restored_at": datetime.now().isoformat()
            }
            
        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"MongoDB restore failed: {str(e)}"
            )
    
    async def restore_full_backup(
        self,
        db_session: AsyncSession,
        mongo_client: AsyncIOMotorClient,
        postgresql_backup: str,
        mongodb_backup: str
    ) -> Dict[str, Any]:
        """
        Restore both PostgreSQL and MongoDB databases from backups.
        
        WARNING: This will delete all existing data in both databases.
        
        Args:
            db_session: Async database session for PostgreSQL
            mongo_client: MongoDB client or database instance
            postgresql_backup: Name of the PostgreSQL backup file
            mongodb_backup: Name of the MongoDB backup directory
            
        Returns:
            dict: Combined restore information for both databases
            
        Raises:
            HTTPException: 500 if restore fails for either database
        """
        
        # Restore PostgreSQL
        pg_result = await self.restore_postgresql_backup(
            db_session,
            postgresql_backup
        )
        
        # Restore MongoDB
        mongo_result = await self.restore_mongodb_backup(
            mongo_client,
            mongodb_backup
        )
        
        return {
            "success": True,
            "postgresql": pg_result,
            "mongodb": mongo_result,
            "restored_at": datetime.now().isoformat()
        }
    
    def delete_backup(self, backup_name: str, backup_type: str) -> Dict[str, Any]:
        """
        Delete a backup file or directory.
        
        Args:
            backup_name: Name of the backup file or directory to delete
            backup_type: Type of backup ('postgresql' or 'mongodb')
            
        Returns:
            dict: Deletion confirmation with backup name and deletion time
            
        Raises:
            HTTPException: 
                - 404 if backup is not found
                - 500 if deletion fails
        """
        backup_path = self._get_backup_path(backup_name)
        
        if not backup_path.exists():
            raise HTTPException(
                status_code=404,
                detail=f"Backup not found: {backup_name}"
            )
        
        try:
            if backup_path.is_dir():
                shutil.rmtree(backup_path)
            else:
                backup_path.unlink()
            
            return {
                "success": True,
                "backup_name": backup_name,
                "deleted_at": datetime.now().isoformat()
            }
            
        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"Failed to delete backup: {str(e)}"
            )


# Global instance
backup_service = BackupService()