from .postgresql import SessionLocal

async def get_postgres_db():
    """
    Async dependency for FastAPI routes to get DB session
    """
    async with SessionLocal() as db:
        try:
            yield db
        finally:
            await db.close()