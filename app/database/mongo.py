from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase
from ..core.config import settings

# Global MongoDB client
mongo_client: AsyncIOMotorClient = None
mongo_db: AsyncIOMotorDatabase = None


def get_mongo_client() -> AsyncIOMotorClient:
    """
    Get MongoDB client instance.
    
    Returns a singleton MongoDB client instance. Creates a new client if one doesn't exist.
    
    Returns:
        AsyncIOMotorClient: MongoDB client instance
    """
    global mongo_client
    if mongo_client is None:
        mongo_client = AsyncIOMotorClient(settings.mongodb_uri)
    return mongo_client


def get_mongo_database() -> AsyncIOMotorDatabase:
    """
    Get MongoDB database instance.
    
    Returns a singleton MongoDB database instance. Creates a new database connection if one doesn't exist.
    
    Returns:
        AsyncIOMotorDatabase: MongoDB database instance
    """
    global mongo_db
    if mongo_db is None:
        client = get_mongo_client()
        mongo_db = client[settings.mongodb_db]
    return mongo_db


async def close_mongo_connection():
    """
    Close MongoDB connection.
    
    Closes the global MongoDB client connection and resets the global variables.
    Should be called during application shutdown.
    """
    global mongo_client, mongo_db
    if mongo_client:
        mongo_client.close()
        mongo_client = None
        mongo_db = None


# For dependency injection - returns the DATABASE, not the client
def get_mongo_db() -> AsyncIOMotorDatabase:
    """
    Dependency for getting MongoDB database instance in FastAPI routes.
    
    Use this in your route dependencies to get the MongoDB database instance.
    Returns the database, not the client.
    
    Returns:
        AsyncIOMotorDatabase: MongoDB database instance
    """
    return get_mongo_database()