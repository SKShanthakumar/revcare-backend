from sql import SessionLocal

def get_sql_db():
    """
    Dependency function for FastAPI endpoints to get database session
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

