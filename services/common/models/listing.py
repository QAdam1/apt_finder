"""Pydantic models for normalized listings."""
from __future__ import annotations

from datetime import date, datetime
from typing import List, Optional

from bson import ObjectId
from pydantic import BaseModel, ConfigDict, Field

from services.common.models.post_raw import PyObjectId


class Coordinates(BaseModel):
    type: str = Field("Point", description="GeoJSON type")
    coordinates: List[float] = Field(default_factory=list, description="[longitude, latitude]")


class Location(BaseModel):
    city: Optional[str] = None
    neighborhood: Optional[str] = None
    street: Optional[str] = None
    coordinates: Optional[Coordinates] = None


class Details(BaseModel):
    rooms: Optional[float] = None
    bathrooms: Optional[float] = None
    size_sqm: Optional[float] = None
    floor: Optional[int] = None
    has_elevator: Optional[bool] = None
    has_parking: Optional[bool] = None
    furnished: Optional[str] = None
    pets_allowed: Optional[bool] = None


class Pricing(BaseModel):
    price: Optional[float] = None
    currency: Optional[str] = None
    maintenance: Optional[float] = None
    property_tax_monthly: Optional[float] = None


class Availability(BaseModel):
    from_date: Optional[date] = None
    min_contract_months: Optional[int] = None


class Meta(BaseModel):
    language: Optional[str] = None
    tags: List[str] = Field(default_factory=list)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)


class Listing(BaseModel):
    """Represents a normalized listing ready for search and RAG."""

    id: Optional[PyObjectId] = Field(default=None, alias="_id")
    source_post_id: Optional[ObjectId] = Field(None, description="Reference to the raw post")
    platform: str = Field(default="facebook")
    url: Optional[str] = None
    title: Optional[str] = None
    description: Optional[str] = None

    location: Location = Field(default_factory=Location)
    details: Details = Field(default_factory=Details)
    pricing: Pricing = Field(default_factory=Pricing)
    availability: Availability = Field(default_factory=Availability)
    meta: Meta = Field(default_factory=Meta)

    embedding: Optional[List[float]] = None
    embedding_model: Optional[str] = None
    embedding_updated_at: Optional[datetime] = None

    model_config = ConfigDict(populate_by_name=True, arbitrary_types_allowed=True)
