PYTHON ?= python
UVICORN ?= uvicorn

.PHONY: help install setup mongo-setup api scraper

help:
@echo "Available targets:"
@echo "  make install       - Install Python dependencies"
@echo "  make mongo-setup   - Create MongoDB indexes (requires env vars)"
@echo "  make setup         - Install deps and initialize Mongo indexes"
@echo "  make api           - Run FastAPI service (uvicorn)"
@echo "  make scraper       - Run Facebook scraper service"

install:
$(PYTHON) -m pip install -r requirements.txt

setup: install mongo-setup

mongo-setup:
$(PYTHON) scripts/setup_mongo.py

api:
$(UVICORN) services.api.app.main:app --reload

scraper:
$(PYTHON) services/scraper/main.py
