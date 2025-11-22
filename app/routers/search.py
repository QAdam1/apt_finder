"""API routes for listing search."""
from __future__ import annotations

from fastapi import APIRouter

from app.schemas.search import SearchListingsRequest, SearchListingsResponse
from app.services.listings_search import search_listings

router = APIRouter(prefix="/search", tags=["search"])


@router.post("/listings", response_model=SearchListingsResponse)
async def search_listings_endpoint(request: SearchListingsRequest) -> SearchListingsResponse:
    """Search listings using vector search and optional filters."""
    return await search_listings(request)
