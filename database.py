from motor.motor_asyncio import AsyncIOMotorClient
from pymongo import ASCENDING, TEXT
from loguru import logger
from config import settings


class Database:
    client: AsyncIOMotorClient = None
    database = None
    collection = None


# Global database instance
database = Database()


async def connect_to_mongo():
    """Create database connection"""
    try:
        database.client = AsyncIOMotorClient(settings.MONGODB_URI)
        database.database = database.client[settings.MONGODB_DATABASE]
        database.collection = database.database[settings.MONGODB_COLLECTION]

        # Test the connection
        await database.client.admin.command('ping')
        logger.info("Connected to MongoDB successfully")

        # Create indexes for better performance
        await create_indexes()

    except Exception as e:
        logger.error(f"Failed to connect to MongoDB: {e}")
        raise


async def close_mongo_connection():
    """Close database connection"""
    if database.client:
        database.client.close()
        logger.info("Disconnected from MongoDB")


async def create_indexes():
    """Create necessary indexes for optimal performance"""
    try:
        # Text index for search functionality
        await database.collection.create_index([
            ("title", TEXT),
            ("content", TEXT),
            ("sourceName", TEXT)
        ])

        # Index for date-based queries
        await database.collection.create_index([("crawledAt", ASCENDING)])

        # Compound index for efficient pagination
        await database.collection.create_index([
            ("crawledAt", ASCENDING),
            ("_id", ASCENDING)
        ])

        logger.info("Database indexes created successfully")

    except Exception as e:
        logger.error(f"Failed to create indexes: {e}")


def get_database():
    """Get database instance - used for dependency injection"""
    return database


db = database
