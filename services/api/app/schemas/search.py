"""Schemas for listing search requests and responses."""
from __future__ import annotations

from datetime import date
from typing import List, Optional

from pydantic import BaseModel, Field


class ListingFilters(BaseModel):
    city: Optional[str] = Field(None)
    neighborhoods: Optional[List[str]] = Field(None)
    price_min: Optional[float] = Field(None)
    price_max: Optional[float] = Field(None)
    rooms_min: Optional[float] = Field(None)
    rooms_max: Optional[float] = Field(None)
    from_date_before: Optional[date] = Field(None)
    from_date_after: Optional[date] = Field(None)


class SearchListingsRequest(BaseModel):
    query: str
    filters: Optional[ListingFilters] = None
    limit: int = Field(default=20, ge=1, le=200)


class ListingSummary(BaseModel):
    id: str
    title: Optional[str] = None
    url: Optional[str] = None
    city: Optional[str] = None
    neighborhood: Optional[str] = None
    price: Optional[float] = None
    rooms: Optional[float] = None
    score: float


class SearchListingsResponse(BaseModel):
    results: List[ListingSummary]
