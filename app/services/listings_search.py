"""Services for searching listings with vector search and filters."""
from __future__ import annotations

from typing import Any, Dict, List

from app.db.mongo import get_database
from app.schemas.search import (
    ListingFilters,
    ListingSummary,
    SearchListingsRequest,
    SearchListingsResponse,
)
from app.services.embedding import embed_text


VECTOR_INDEX_NAME = "listing_embedding_index"


def _build_filter(filters: ListingFilters | None) -> Dict[str, Any]:
    """Convert ListingFilters into a MongoDB filter document."""
    if not filters:
        return {}

    query: Dict[str, Any] = {}

    if filters.city:
        query["location.city"] = filters.city
    if filters.neighborhoods:
        query["location.neighborhood"] = {"$in": filters.neighborhoods}

    price_clause: Dict[str, Any] = {}
    if filters.price_min is not None:
        price_clause["$gte"] = filters.price_min
    if filters.price_max is not None:
        price_clause["$lte"] = filters.price_max
    if price_clause:
        query["pricing.price"] = price_clause

    rooms_clause: Dict[str, Any] = {}
    if filters.rooms_min is not None:
        rooms_clause["$gte"] = filters.rooms_min
    if filters.rooms_max is not None:
        rooms_clause["$lte"] = filters.rooms_max
    if rooms_clause:
        query["details.rooms"] = rooms_clause

    date_clause: Dict[str, Any] = {}
    if filters.from_date_after is not None:
        date_clause["$gte"] = filters.from_date_after
    if filters.from_date_before is not None:
        date_clause["$lte"] = filters.from_date_before
    if date_clause:
        query["availability.from_date"] = date_clause

    return query


async def search_listings(request: SearchListingsRequest) -> SearchListingsResponse:
    """Perform a vector search with optional filters and return listing summaries."""
    db = get_database()
    listings_collection = db["listings"]

    query_embedding = await embed_text(request.query)
    filters = _build_filter(request.filters)

    pipeline = [
        {
            "$vectorSearch": {
                "index": VECTOR_INDEX_NAME,
                "path": "embedding",
                "queryVector": query_embedding,
                "numCandidates": max(request.limit * 5, 50),
                "limit": request.limit,
                "filter": filters or None,
            }
        },
        {
            "$project": {
                "title": 1,
                "url": 1,
                "location.city": 1,
                "location.neighborhood": 1,
                "pricing.price": 1,
                "details.rooms": 1,
                "score": {"$meta": "vectorSearchScore"},
            }
        },
    ]

    cursor = listings_collection.aggregate(pipeline)
    results: List[ListingSummary] = []
    async for doc in cursor:
        results.append(
            ListingSummary(
                id=str(doc.get("_id")),
                title=doc.get("title"),
                url=doc.get("url"),
                city=doc.get("location", {}).get("city") if doc.get("location") else None,
                neighborhood=doc.get("location", {}).get("neighborhood") if doc.get("location") else None,
                price=doc.get("pricing", {}).get("price") if doc.get("pricing") else None,
                rooms=doc.get("details", {}).get("rooms") if doc.get("details") else None,
                score=float(doc.get("score", 0.0)),
            )
        )

    return SearchListingsResponse(results=results)
