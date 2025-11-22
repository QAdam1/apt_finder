"""Setup MongoDB collections and indexes for the apartment hunter project."""
import asyncio
from typing import Any

from app.db.mongo import close_mongo_connection, connect_to_mongo, get_database


EMBEDDING_DIMENSIONS = 1536
VECTOR_INDEX_NAME = "listing_embedding_index"


async def create_posts_raw_indexes(db: Any) -> None:
    """Create indexes for the posts_raw collection."""
    await db.posts_raw.create_index("source.post_id", unique=True)
    await db.posts_raw.create_index("posted_at")
    await db.posts_raw.create_index("scraped_at")
    print("Ensured indexes on posts_raw")


async def create_listings_indexes(db: Any) -> None:
    """Create indexes for the listings collection, including vector search."""
    await db.listings.create_index("location.city")
    await db.listings.create_index("location.neighborhood")
    await db.listings.create_index("pricing.price")
    await db.listings.create_index("details.rooms")
    await db.listings.create_index("availability.from_date")
    print("Ensured standard indexes on listings")

    # Atlas Vector Search index
    try:
        await db.command(
            {
                "createSearchIndexes": "listings",
                "indexes": [
                    {
                        "name": VECTOR_INDEX_NAME,
                        "definition": {
                            "fields": {
                                "embedding": {
                                    "type": "vector",
                                    "path": "embedding",
                                    "numDimensions": EMBEDDING_DIMENSIONS,
                                    "similarity": "cosine",
                                }
                            }
                        },
                    }
                ],
            }
        )
        print(f"Ensured vector index '{VECTOR_INDEX_NAME}' on listings.embedding")
    except Exception as exc:  # noqa: BLE001
        print(
            "Warning: could not create vector index automatically. "
            "If using Atlas, ensure you have permissions and retry via the UI.",
        )
        print(f"Details: {exc}")


async def main() -> None:
    """Connect to MongoDB and create required collections and indexes."""
    await connect_to_mongo()
    db = get_database()

    await create_posts_raw_indexes(db)
    await create_listings_indexes(db)

    await close_mongo_connection()


if __name__ == "__main__":
    asyncio.run(main())
