"""FastAPI application entrypoint."""
from __future__ import annotations

import sys
from pathlib import Path

from fastapi import FastAPI

# Ensure repository root is on sys.path when running as a script.
ROOT_DIR = Path(__file__).resolve().parents[1]
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from app.db.mongo import close_mongo_connection, connect_to_mongo
from app.routers import search as search_router

app = FastAPI(title="AI Apartment Hunter")


@app.on_event("startup")
async def startup_event() -> None:
    await connect_to_mongo()


@app.on_event("shutdown")
async def shutdown_event() -> None:
    await close_mongo_connection()


app.include_router(search_router.router)
