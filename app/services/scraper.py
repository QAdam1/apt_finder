"""Service for scraping Facebook groups into PostRaw entries."""
from __future__ import annotations

import asyncio
from datetime import datetime
from typing import Dict, Iterable, List, Optional

from facebook_scraper import get_posts
from pymongo.errors import BulkWriteError

from app.db.mongo import get_database
from app.models.post_raw import PostRaw, RawContent, SourceInfo


async def _collect_posts(
    group: str, pages: int, cookies: Optional[str], request_kwargs: Dict[str, object]
) -> List[Dict[str, object]]:
    """Collect posts from facebook-scraper in a thread executor."""

    def _fetch() -> List[Dict[str, object]]:
        return list(get_posts(group=group, pages=pages, cookies=cookies, **request_kwargs))

    loop = asyncio.get_running_loop()
    return await loop.run_in_executor(None, _fetch)


def _map_to_post_raw(
    raw_post: Dict[str, object], group: str, group_name: Optional[str]
) -> PostRaw:
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
    cookies: Optional[str] = None,
    group_name: Optional[str] = None,
    request_kwargs: Optional[Dict[str, object]] = None,
) -> List[PostRaw]:
    """Scrape posts from a Facebook group and return PostRaw objects."""
    raw_posts = await _collect_posts(group, pages, cookies, request_kwargs or {})
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
