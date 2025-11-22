# AI Apartment Hunter Monorepo

A monorepo containing microservices for ingesting Facebook rental posts, normalizing them into structured listings with embeddings, and exposing search APIs.

## Services
- **API** (`services/api`): FastAPI app exposing listing search endpoints backed by MongoDB + Atlas Vector Search.
- **Scraper** (`services/scraper`): Polls Facebook groups using [`facebook-scraper`](https://github.com/kevinzg/facebook-scraper) and stores raw posts in MongoDB.
- **Common** (`services/common`): Shared configuration, MongoDB client, models, and embedding helper.

## Quickstart (with Makefile)
1. **Create virtualenv + install deps**
   ```bash
   make install   # creates .venv (Python 3) and installs requirements into it
   ```

2. **Configure environment** (`.env`)
   ```bash
   cat > .env <<'ENV'
   MONGO_URI=mongodb+srv://<user>:<pass>@<cluster>/<db>?retryWrites=true&w=majority
   MONGO_DB_NAME=apt_finder
   OPENAI_API_KEY=<your_openai_key>
   # Scraper
   FACEBOOK_EMAIL=<fb_email>
   FACEBOOK_PASSWORD=<fb_password>
   FACEBOOK_GROUP_ID=<facebook_group_numeric_id_or_handle>
   FACEBOOK_PAGES=1
   FACEBOOK_POLL_INTERVAL_SECONDS=900
   ENV
   ```

3. **Initialize Mongo indexes**
   ```bash
   make mongo-setup
   ```

4. **Run the API service**
   ```bash
   make api
   ```
   - Base URL: `http://127.0.0.1:8000`
   - Example: `POST /search/listings` with `{"query": "2 bedroom in Tel Aviv", "limit": 10}`.

5. **Run the scraper service (alongside the API)**
   ```bash
   make scraper
   ```
   - Uses `FACEBOOK_*` env vars for credentials and group id.
   - Scrapes once on startup, then polls every `FACEBOOK_POLL_INTERVAL_SECONDS` seconds.

6. **Clean the virtualenv (optional)**
   ```bash
   make clean
   ```

### If `make` is unavailable (e.g., on Windows shells)
Run the equivalent commands manually from the repo root (after activating your virtualenv):
```bash
python -m venv .venv
# POSIX: source .venv/bin/activate
# Windows: .venv\Scripts\activate
python -m pip install -r requirements.txt
python scripts/setup_mongo.py
uvicorn services.api.app.main:app --reload
# In another shell if desired
python services/scraper/main.py
```

## Repository layout
```
services/
  api/            # FastAPI microservice
    app/
      main.py
      routers/search.py
      schemas/search.py
      services/listings_search.py
  scraper/        # Facebook scraping microservice
    main.py
    service.py
  common/         # Shared code
    config.py
    db.py
    models/
    services/embedding.py
scripts/
  setup_mongo.py  # Creates indexes including the Atlas vector index
requirements.txt
```

## Notes
- The vector index expected by the API is `listing_embedding_index` on `listings.embedding`.
- The scraper tolerates duplicate insert attempts when posts already exist.
- Both services rely on the shared `.env` configuration in the repository root.
- The `facebook-scraper` dependency requires `lxml[html_clean]`, which is included in `requirements.txt`; ensure your environment installs wheels or build dependencies for `lxml`.
