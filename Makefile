SHELL := /bin/bash

.PHONY: help install api scraper mongo-setup clean

help:
@echo "Available targets:"
@echo "  make install      - Install Node workspace dependencies"
@echo "  make api          - Run the Fastify API"
@echo "  make scraper      - Run the Facebook scraper"
@echo "  make mongo-setup  - Create Mongo indexes via python script"
@echo "  make clean        - Remove node_modules"

install:
npm install

api:
npm run --workspace services/api start

scraper:
npm run --workspace services/scraper start

mongo-setup:
npm run setup:mongo

clean:
rm -rf node_modules services/*/node_modules package-lock.json
