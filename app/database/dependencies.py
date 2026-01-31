from contextlib import asynccontextmanager
from .postgresql import SessionLocal
from .mongo import get_mongo_database as get_mongo_db, get_mongo_client

async def get_postgres_db():
    """
    Async dependency for FastAPI routes to get database session.
    
    Provides a database session that is automatically closed after the request.
    Use this as a dependency in FastAPI route handlers.
    
    Yields:
        AsyncSession: Database session instance
    """
    async with SessionLocal() as db:
        try:
            yield db
        finally:
            await db.close()

@asynccontextmanager
async def db_session():
    """ Used to get postgresql session without dependency injection """
    async with SessionLocal() as db:
        yield db
    