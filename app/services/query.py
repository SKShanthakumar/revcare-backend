from datetime import datetime
from bson import ObjectId
from fastapi import HTTPException
from motor.motor_asyncio import AsyncIOMotorDatabase
from sqlalchemy.ext.asyncio import AsyncSession as Session
from app.models import Query
from app.schemas import QueryCreate, QueryResponse
from app.services import notification as notification_service

async def create_query_service(db: AsyncIOMotorDatabase, data: QueryCreate) -> Query:
    """
    Create a new customer query.
    
    Args:
        db: MongoDB database session
        data: Query creation data with customer email and query text
        
    Returns:
        Query: Created query document
    """
    query_doc = Query(customer_email=data.customer_email, query=data.query_text)
    result = await db.queries.insert_one(query_doc.model_dump(by_alias=True))
    created = await db.queries.find_one({"_id": result.inserted_id})
    return created


async def respond_to_query_service(
    db: AsyncIOMotorDatabase,
    pg_db: Session,
    query_id: str,
    data: QueryResponse,
    user_payload: dict
) -> Query:
    """
    Respond to a customer query (admin only).
    
    Updates the query with admin's response and sends notification email to customer.
    
    Args:
        db: MongoDB database session
        pg_db: PostgreSQL database session for notifications
        query_id: Query ID to respond to
        data: Query response data with response text
        user_payload: Token payload containing user_id of the responder
        
    Returns:
        Query: Updated query document
        
    Raises:
        HTTPException: 
            - 400 if query_id is invalid
            - 404 if query is not found
    """
    if not ObjectId.is_valid(query_id):
        raise HTTPException(status_code=400, detail="Invalid query ID")

    result = await db.queries.update_one(
        {"_id": ObjectId(query_id)},
        {
            "$set": {
                "response": data.response,
                "responded_by": user_payload.get("user_id"),
                "responded_at": datetime.utcnow(),
            }
        },
    )

    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Query not found")
    

    updated = await db.queries.find_one({"_id": ObjectId(query_id)})
    await notification_service.send_query_response(pg_db, updated.get('customer_email'), updated.get('query'), updated.get('response'))

    return updated


async def get_all_queries_service(db: AsyncIOMotorDatabase):
    """
    Fetch all queries (admin access).
    
    Retrieves all customer queries sorted by creation date (newest first).
    
    Args:
        db: MongoDB database session
        
    Returns:
        list: List of all query documents
    """
    cursor = db.queries.find().sort("created_at", -1)
    queries = await cursor.to_list(None)
    return queries
