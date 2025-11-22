"""Entrypoint for the scraper microservice."""
from __future__ import annotations

import asyncio
import sys
from pathlib import Path

# Ensure repository root is on sys.path when running as a script.
ROOT_DIR = Path(__file__).resolve().parents[2]
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from services.common.config import settings
from services.common.db import close_mongo_connection, connect_to_mongo
from services.scraper.service import poll_and_store, scrape_and_store_once


async def main() -> None:
    await connect_to_mongo()
    try:
        await scrape_and_store_once()
        await poll_and_store(settings.facebook_poll_interval_seconds)
    finally:
        await close_mongo_connection()


if __name__ == "__main__":
    asyncio.run(main())
