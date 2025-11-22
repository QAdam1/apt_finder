"""Service for scraping Facebook groups into PostRaw entries."""
from __future__ import annotations

import asyncio
from datetime import datetime
from typing import Dict, Iterable, List, Optional, Tuple

from facebook_scraper import get_posts
from pymongo.errors import BulkWriteError

from services.common.config import settings
from services.common.db import get_database
from services.common.models.post_raw import PostRaw, RawContent, SourceInfo


async def _collect_posts(
    group: str,
    pages: int,
    credentials: Optional[Tuple[str, str]],
    request_kwargs: Dict[str, object],
) -> List[Dict[str, object]]:
    """Collect posts from facebook-scraper in a thread executor."""

    def _fetch() -> List[Dict[str, object]]:
        return list(
            get_posts(
                group=group,
                pages=pages,
                credentials=credentials,
                **request_kwargs,
            )
        )

    loop = asyncio.get_running_loop()
    return await loop.run_in_executor(None, _fetch)


def _map_to_post_raw(raw_post: Dict[str, object], group: str, group_name: Optional[str]) -> PostRaw:
    """Map facebook-scraper dict to PostRaw model."""
    images: List[str] = []
    if raw_post.get("images"):
        images = list(raw_post.get("images", []))
    elif raw_post.get("image"):
        images = [str(raw_post.get("image"))]

    return PostRaw(
        source=SourceInfo(
            platform="facebook",
            group_id=group,
            group_name=group_name,
            post_id=str(raw_post.get("post_id")) if raw_post.get("post_id") else None,
            url=str(raw_post.get("post_url")) if raw_post.get("post_url") else None,
        ),
        raw=RawContent(
            text=str(raw_post.get("post_text") or raw_post.get("text") or "") or None,
            html=None,
            images=images,
            author_name=str(raw_post.get("username")) if raw_post.get("username") else None,
            author_id=str(raw_post.get("user_id")) if raw_post.get("user_id") else None,
        ),
        posted_at=raw_post.get("time") or None,
        scraped_at=datetime.utcnow(),
    )


async def scrape_group_posts(
    group: str,
    *,
    pages: int = 1,
    credentials: Optional[Tuple[str, str]] = None,
    group_name: Optional[str] = None,
    request_kwargs: Optional[Dict[str, object]] = None,
) -> List[PostRaw]:
    """Scrape posts from a Facebook group and return PostRaw objects."""
    raw_posts = await _collect_posts(group, pages, credentials, request_kwargs or {})
    return [_map_to_post_raw(raw_post, group, group_name) for raw_post in raw_posts]


async def persist_raw_posts(posts: Iterable[PostRaw]) -> List[str]:
    """Insert raw posts into MongoDB, skipping duplicates gracefully."""
    posts_list = list(posts)
    if not posts_list:
        return []

    db = get_database()
    collection = db["posts_raw"]
    payload = [post.model_dump(by_alias=True, exclude_none=True) for post in posts_list]

    try:
        result = await collection.insert_many(payload, ordered=False)
        inserted_ids = [str(_id) for _id in result.inserted_ids]
    except BulkWriteError as exc:  # duplicates are expected sometimes
        inserted_ids = [str(doc.get("_id")) for doc in exc.details.get("writeErrors", []) if doc]

    return inserted_ids


async def scrape_and_store_once() -> List[str]:
    """Scrape configured group once and persist results."""
    if not settings.facebook_group_id:
        raise ValueError("FACEBOOK_GROUP_ID is required to run the scraper service.")

    credentials: Optional[Tuple[str, str]] = None
    if settings.facebook_email and settings.facebook_password:
        credentials = (settings.facebook_email, settings.facebook_password)

    posts = await scrape_group_posts(
        settings.facebook_group_id,
        pages=settings.facebook_pages,
        credentials=credentials,
        group_name=None,
        request_kwargs=settings.facebook_request_kwargs,
    )
    return await persist_raw_posts(posts)


async def poll_and_store(interval_seconds: int) -> None:
    """Continuously poll the configured group and store new posts."""
    while True:
        await scrape_and_store_once()
        await asyncio.sleep(interval_seconds)
