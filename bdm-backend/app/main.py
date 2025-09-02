
from fastapi import FastAPI, Depends, Query
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from datetime import date
from typing import Optional

from .config import settings
from .database import SessionLocal, init_db
from .models import Price
from .schemas import MetricsSummary, SeriesResponse, MetricPoint, AlertState
from .compute import fetch_prices_df, compute_td_te
from .ingest import ingest_pair

app = FastAPI(title="Benchmark Drift Monitor", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

async def get_db():
    async with SessionLocal() as session:
        yield session

@app.on_event("startup")
async def on_startup():
    await init_db()

@app.get("/health")
async def health():
    return {"status": "ok"}

@app.post("/ingest/run")
async def run_ingest(
    fund: str = Query(..., description="Fund symbol, e.g., SPY"),
    benchmark: str = Query(..., description="Benchmark symbol, e.g., ^GSPC"),
    days: int = Query(120, ge=30, le=1000),
    db: AsyncSession = Depends(get_db),
):
    n = await ingest_pair(db, fund=fund, benchmark=benchmark, days=days)
    return {"ingested": n, "fund": fund, "benchmark": benchmark}

@app.get("/metrics/series", response_model=SeriesResponse)
async def metrics_series(
    fund: str, benchmark: str, window: int = Query(default=settings.te_window_days, ge=5, le=252),
    db: AsyncSession = Depends(get_db),
):
    df = await fetch_prices_df(db, [fund, benchmark])
    ret, td_mean_bps, te_bps = compute_td_te(df, fund, benchmark, window=window)
    points = []
    if ret is not None and not ret.empty:
        for dt, row in ret.iterrows():
            points.append(MetricPoint(date=dt, fund_ret=float(row[fund]), bench_ret=float(row[benchmark]), td=float(row["td"])))
    return SeriesResponse(points=points)

@app.get("/metrics/summary", response_model=MetricsSummary)
async def metrics_summary(
    fund: str, benchmark: str, window: int = Query(default=settings.te_window_days, ge=5, le=252),
    db: AsyncSession = Depends(get_db),
):
    df = await fetch_prices_df(db, [fund, benchmark])
    ret, td_mean_bps, te_bps = compute_td_te(df, fund, benchmark, window=window)
    return MetricsSummary(window=window, td_mean_bps=td_mean_bps or 0.0, te_bps=te_bps or 0.0, count=0 if ret is None else len(ret))

@app.get("/alerts", response_model=AlertState)
async def alerts(
    fund: str, benchmark: str, window: int = Query(default=settings.te_window_days, ge=5, le=252),
    db: AsyncSession = Depends(get_db),
):
    df = await fetch_prices_df(db, [fund, benchmark])
    ret, td_mean_bps, te_bps = compute_td_te(df, fund, benchmark, window=window)
    latest_td_bps: Optional[float] = None
    if ret is not None and not ret.empty:
        latest_td_bps = float(ret["td"].iloc[-1] * 1e4)
    td_breach = latest_td_bps is not None and abs(latest_td_bps) > settings.td_threshold_bps
    te_breach = te_bps is not None and te_bps > settings.te_threshold_bps
    return AlertState(
        td_breach=td_breach,
        te_breach=te_breach,
        td_threshold_bps=settings.td_threshold_bps,
        te_threshold_bps=settings.te_threshold_bps,
        window=window,
        latest_td_bps=latest_td_bps,
    )
