from .postgresql import SessionLocal
from .mongo import get_database as get_mongo_db

async def get_postgres_db():
    """
    Async dependency for FastAPI routes to get DB session
    """
    async with SessionLocal() as db:
        try:
            yield db
        finally:
            await db.close()