from typing import List
from fastapi import APIRouter, Depends, Security, status, BackgroundTasks
from motor.motor_asyncio import AsyncIOMotorDatabase
from sqlalchemy.ext.asyncio import AsyncSession as Session
from app.auth.dependencies import validate_token
from app.database.dependencies import get_mongo_db, get_postgres_db
from app.models import Query
from app.schemas import QueryCreate, QueryResponse
from app.services.query import create_query_service, respond_to_query_service, get_all_queries_service

router = APIRouter()


# Create query - by customer
@router.post("/", response_model=Query, status_code=status.HTTP_201_CREATED)
async def create_query(
    payload: QueryCreate,
    db: AsyncIOMotorDatabase = Depends(get_mongo_db),
) -> Query:
    """
    Create a new customer query.
    
    Args:
        payload: Query creation data
        db: MongoDB database session
        
    Returns:
        Query: Created query instance
    """
    return await create_query_service(db, payload)


# Respond to query - by admin
@router.put("/{query_id}/respond", response_model=Query)
async def respond_to_query(
    query_id: str,
    payload: QueryResponse,
    background_tasks: BackgroundTasks,
    user_payload: dict = Security(validate_token, scopes=["UPDATE:QUERIES"]),
    db: AsyncIOMotorDatabase = Depends(get_mongo_db),
    pg_db: Session = Depends(get_postgres_db)
) -> Query:
    """
    Respond to a specific customer query (admin only).
    
    Args:
        query_id: Query ID to respond to
        payload: Query response data
        user_payload: Validated token payload
        db: MongoDB database session
        pg_db: PostgreSQL database session
        
    Returns:
        Query: Updated query with response
    """
    return await respond_to_query_service(db, pg_db, query_id, payload, user_payload, background_tasks)


# Get all queries - by admin
@router.get("/", response_model=List[Query])
async def get_all_queries(
    user_payload: dict = Security(validate_token, scopes=["READ:QUERIES"]),
    db: AsyncIOMotorDatabase = Depends(get_mongo_db),
) -> List[Query]:
    """
    Retrieve all customer queries.
    
    Args:
        user_payload: Validated token payload
        db: MongoDB database session
        
    Returns:
        List[Query]: List of all customer queries
    """
    return await get_all_queries_service(db)
