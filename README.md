# AI Apartment Hunter

Backend for ingesting Facebook rental posts, normalizing them into structured listings, embedding them, and exposing FastAPI search endpoints.

## Prerequisites
- Python 3.11+
- MongoDB cluster/Atlas URI with vector search (for embeddings)
- OpenAI API key

## Environment setup
```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

# Provide connection + API keys
cat > .env <<'ENV'
MONGO_URI=mongodb+srv://<user>:<pass>@<cluster>/<db>?retryWrites=true&w=majority
MONGO_DB_NAME=apt_finder
OPENAI_API_KEY=<your_openai_key>
ENV
```

## Initialize Mongo indexes
```bash
python scripts/setup_mongo.py
```
Creates indexes on `posts_raw` and `listings`, and attempts to create the Atlas vector index `listing_embedding_index`.

## Run the API
```bash
uvicorn app.main:app --reload
```
FastAPI serves at `http://127.0.0.1:8000`. POST `/search/listings` with a JSON body to query listings.

## Scrape Facebook posts (optional)
The scraper helper wraps [`facebook-scraper`](https://github.com/kevinzg/facebook-scraper).
Example to fetch posts and store them:
```bash
python - <<'PY'
import asyncio
from app.services.scraper import persist_raw_posts, scrape_group_posts
from app.db.mongo import connect_to_mongo, close_mongo_connection

async def main():
    await connect_to_mongo()
    posts = await scrape_group_posts("some-group-handle", pages=1, cookies="/path/to/cookies.txt")
    inserted_ids = await persist_raw_posts(posts)
    print("Inserted IDs", inserted_ids)
    await close_mongo_connection()

asyncio.run(main())
PY
```
Provide cookies if the group requires login. Scraped posts will be written to `posts_raw`.
