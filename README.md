
# Benchmark Drift Monitor (BDM)

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

