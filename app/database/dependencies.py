from .postgresql import SessionLocal

def get_postgres_db():
    """
    Dependency function for FastAPI endpoints to get database session
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

