"""Pydantic models for raw social posts."""
from __future__ import annotations

from datetime import datetime
from typing import List, Optional

from bson import ObjectId
from pydantic import BaseModel, ConfigDict, Field


class PyObjectId(ObjectId):
    """Custom ObjectId field for Pydantic models."""

    @classmethod
    def __get_validators__(cls):  # type: ignore[override]
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if isinstance(v, ObjectId):
            return v
        if isinstance(v, str) and ObjectId.is_valid(v):
            return ObjectId(v)
        raise TypeError("Invalid ObjectId")


class SourceInfo(BaseModel):
    platform: str = Field(..., description="Source platform, e.g., facebook")
    group_id: Optional[str] = Field(None, description="Identifier of the group")
    group_name: Optional[str] = Field(None, description="Name of the group")
    post_id: Optional[str] = Field(None, description="Platform-specific post id")
    url: Optional[str] = Field(None, description="URL to the post")


class RawContent(BaseModel):
    text: Optional[str] = Field(None, description="Raw text content")
    html: Optional[str] = Field(None, description="Raw HTML content")
    images: List[str] = Field(default_factory=list, description="List of image URLs")
    author_name: Optional[str] = Field(None, description="Author display name")
    author_id: Optional[str] = Field(None, description="Platform-specific author id")


class StatusInfo(BaseModel):
    is_active: bool = Field(default=True)
    last_seen_at: Optional[datetime] = Field(None)
    deleted_at: Optional[datetime] = Field(None)


class PostRaw(BaseModel):
    """Represents a raw scraped social post."""

    id: Optional[PyObjectId] = Field(default=None, alias="_id")
    source: SourceInfo
    raw: RawContent
    posted_at: Optional[datetime] = Field(None)
    scraped_at: datetime = Field(default_factory=datetime.utcnow)
    status: StatusInfo = Field(default_factory=StatusInfo)

    model_config = ConfigDict(populate_by_name=True, arbitrary_types_allowed=True)
