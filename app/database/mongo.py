from motor.motor_asyncio import AsyncIOMotorClient
from ..core.config import settings

client: AsyncIOMotorClient | None = None
db = None

async def init_mongo_on_startup():
    """Initialize MongoDB connection when the app starts."""
    global client, db
    client = AsyncIOMotorClient(settings.mongodb_uri)
    db = client[settings.mongodb_db]

async def close_mongo_connection():
    """Close MongoDB connection on app shutdown."""
    global client
    if client:
        client.close()

def get_database():
    """Get the current database instance."""
    global db
    if db is None:
        raise RuntimeError("Database not initialized.")
    return db
