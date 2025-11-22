"""Embedding service wrapping OpenAI embeddings API."""
from __future__ import annotations

import asyncio
from typing import List

from openai import OpenAI

from app.core.config import settings

EMBEDDING_MODEL = "text-embedding-3-small"

_client = OpenAI(api_key=settings.openai_api_key)


async def embed_text(text: str) -> List[float]:
    """Generate an embedding vector for the given text."""

    def _embed() -> List[float]:
        response = _client.embeddings.create(model=EMBEDDING_MODEL, input=text)
        return response.data[0].embedding

    return await asyncio.to_thread(_embed)
