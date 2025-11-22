SHELL := /bin/bash
.RECIPEPREFIX := >

# Virtualenv config (supports Windows and POSIX paths)
VENV ?= .venv
ifeq ($(OS),Windows_NT)
VENV_BIN := $(VENV)/Scripts
else
VENV_BIN := $(VENV)/bin
endif

# Base Python used to create the venv (falls back to python3 or python)
PYTHON_CMD ?= $(shell command -v python3 || command -v python)
PYTHON := $(VENV_BIN)/python
UVICORN := $(VENV_BIN)/uvicorn

.DEFAULT_GOAL := help

.PHONY: help venv install setup mongo-setup api scraper clean

help:
> @echo "Available targets:"
> @echo "  make venv          - Create virtualenv in $(VENV) (uses $(PYTHON_CMD))"
> @echo "  make install       - Install Python dependencies into $(VENV)"
> @echo "  make mongo-setup   - Create MongoDB indexes (requires env vars)"
> @echo "  make setup         - Create venv, install deps, initialize Mongo indexes"
> @echo "  make api           - Run FastAPI service (uvicorn) from the venv"
> @echo "  make scraper       - Run Facebook scraper service from the venv"
> @echo "  make clean         - Remove the virtualenv"

venv:
> @test -d "$(VENV_BIN)" || "$(PYTHON_CMD)" -m venv "$(VENV)"
> "$(PYTHON)" -m pip install --upgrade pip

install: venv
> "$(PYTHON)" -m pip install -r requirements.txt

setup: install mongo-setup

mongo-setup:
> "$(PYTHON)" scripts/setup_mongo.py

api:
> "$(UVICORN)" services.api.app.main:app --reload

scraper:
> "$(PYTHON)" services/scraper/main.py

clean:
> rm -rf "$(VENV)"
