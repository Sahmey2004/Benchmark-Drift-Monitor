
# Benchmark Drift Monitor (BDM) — Starter

A small, cloud-friendly data app that ingests daily fund/benchmark prices, computes tracking difference (TD) and rolling tracking error (TE), and flags drift when thresholds are breached. It exposes a typed API and a simple, accessible dashboard.

Features

Ingest daily adjusted close prices for a fund and its benchmark.

Compute TD (fund return − benchmark return) and rolling TE (stdev of TD over N days), both in basis points.

Alert when TD/TE cross configurable thresholds.

API with OpenAPI docs; React dashboard with charts and an “Explain Drift (lite)” panel.

Dev UX: Docker Compose, CI-ready structure, unit tests for core metrics.
 Includes:
- **Backend**: FastAPI + SQLAlchemy (PostgreSQL by default; SQLite fallback) with endpoints for ingest/metrics/alerts.
- **Frontend**: React + TypeScript (Vite) with accessible charts and an "Explain Drift" panel.
- **Infra**: Docker Compose for DB + backend + frontend (dev).

## Quick Start (Local, minimal)
> Requires Python 3.10+, Node 18+, and optionally Docker.

### 1) Backend
```bash
cd bdm-backend
python -m venv .venv && source .venv/bin/activate  # or .venv\Scripts\activate on Windows
pip install -r requirements.txt
cp .env.sample .env  # edit as needed; defaults to SQLite for quick start
uvicorn app.main:app --reload
```
Open API docs: http://localhost:8000/docs

Seed some data (SPY vs ^GSPC):
```bash
curl -X POST "http://localhost:8000/ingest/run?fund=SPY&benchmark=%5EGSPC&days=120"
```

View metrics:
```bash
curl "http://localhost:8000/metrics/summary?fund=SPY&benchmark=%5EGSPC&window=30"
```

### 2) Frontend
```bash
cd ../bdm-frontend
npm install
npm run dev
```
Open http://localhost:5173

### 3) Docker (optional end‑to‑end)
```bash
# From repo root
cp .env.sample .env
docker compose up --build
# Backend: http://localhost:8000/docs
# Frontend: http://localhost:5173
# Postgres: localhost:5432 (user: bdm, password: bdm, db: bdm)
```

## What’s Implemented
- **/ingest/run**: pulls daily OHLC via yfinance for `fund` and `benchmark` and stores adjusted close.
- **/metrics/summary**: computes TD series and rolling TE (std of TD over N days), plus basic attribution stubs.
- **/alerts**: evaluates TD/TE against thresholds; returns current alert state.
- **Observability**: request logging + simple metrics counters in memory (stubbed for demo).
- **Testing**: unit tests for metrics logic.

## Notes
- For speed, this starter defaults to SQLite. Switching to Postgres is one env var change (see `.env.sample`).
- Attribution is intentionally **lite**; extend with holdings-based active share, fees, dividend timing, etc.
- This is a scaffold built to learn & demo craft: clean APIs, tests, docs, and a small but real UX.
