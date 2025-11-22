"""FastAPI application entrypoint."""
from __future__ import annotations

from fastapi import FastAPI

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
