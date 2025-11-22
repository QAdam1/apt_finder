"""FastAPI application entrypoint."""
from __future__ import annotations

import sys
from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI

# Ensure repository root is on sys.path when running as a script.
ROOT_DIR = Path(__file__).resolve().parents[3]
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from services.common.db import close_mongo_connection, connect_to_mongo
from services.api.app.routers import search as search_router


@asynccontextmanager
async def lifespan(_: FastAPI):
    await connect_to_mongo()
    try:
        yield
    finally:
        await close_mongo_connection()


app = FastAPI(title="AI Apartment Hunter", lifespan=lifespan)

app.include_router(search_router.router)
