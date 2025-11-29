# AI Apartment Hunter (Node.js Monorepo)

This repo hosts two Node.js microservices plus shared utilities:

- **API** (`services/api`): Fastify server exposing `/search/listings`.
- **Scraper** (`services/scraper`): polls Facebook groups via the `facebook-scraper` Python package and stores posts in MongoDB.
- **Common** (`services/common`): shared config, Mongo, embeddings, and helpers.

## Requirements

- Node.js 18+
- Python 3 (for the facebook-scraper helper)
- MongoDB (Atlas or local) with a vector index named `listing_embedding_index` on `listings.embedding`.

Install the Python dependency:

```bash
pip install facebook-scraper
```

## Installation

```bash
npm install
```

The root `package.json` uses npm workspaces to install dependencies for all services.

## Environment

Create `.env` in the repository root:

```
MONGO_URI=mongodb+srv://...
MONGO_DB_NAME=apt_finder
OPENAI_API_KEY=sk-...
SCRAPER_GROUP_ID=your_facebook_group_id
SCRAPER_EMAIL=your_email
SCRAPER_PASSWORD=your_password
SCRAPER_INTERVAL_SECONDS=300
```

## Running the API

```bash
npm run --workspace services/api start
```

The API listens on `PORT` (default 8000) and exposes `POST /search/listings`.

## Running the scraper

```bash
npm run --workspace services/scraper start
```

The scraper triggers immediately and then every `SCRAPER_INTERVAL_SECONDS` seconds. It inserts into `posts_raw`, ignoring duplicate post IDs.

## Mongo indexes

Create the indexes (including the Atlas vector index) via the Node helper:

```bash
npm run setup:mongo
```

## Manual search request

```bash
curl -X POST http://localhost:8000/search/listings \
  -H 'Content-Type: application/json' \
  -d '{"query":"2 bedroom in Tel Aviv","limit":5}'
```
