"""MongoDB connection management using Motor."""
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase

from app.core.config import settings


client: AsyncIOMotorClient | None = None
_db: AsyncIOMotorDatabase | None = None


def get_database() -> AsyncIOMotorDatabase:
    """Expose the active MongoDB database instance."""
    if _db is None:
        raise RuntimeError("Database not initialized. Call connect_to_mongo first.")
    return _db


async def connect_to_mongo() -> None:
    """Establish the MongoDB client and database references."""
    global client, _db
    client = AsyncIOMotorClient(settings.mongo_uri)
    _db = client[settings.mongo_db_name]


async def close_mongo_connection() -> None:
    """Close the MongoDB connection if it exists."""
    global client, _db
    if client:
        client.close()
    client = None
    _db = None
