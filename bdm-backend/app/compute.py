
from __future__ import annotations
import pandas as pd
import numpy as np
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from .models import Price

def _pct_change(s: pd.Series) -> pd.Series:
    return s.pct_change().fillna(0.0)

async def fetch_prices_df(db: AsyncSession, symbols: list[str]) -> pd.DataFrame:
    stmt = select(Price).where(Price.symbol.in_(symbols))
    rows = (await db.execute(stmt)).scalars().all()
    if not rows:
        return pd.DataFrame()
    df = pd.DataFrame([{"symbol": r.symbol, "date": r.date, "adj_close": r.adj_close} for r in rows])
    df = df.pivot(index="date", columns="symbol", values="adj_close").sort_index()
    return df

def compute_td_te(df: pd.DataFrame, fund: str, benchmark: str, window: int = 30):
    if df.empty or fund not in df.columns or benchmark not in df.columns:
        return pd.DataFrame(), None, None

    ret = df[[fund, benchmark]].apply(_pct_change)
    ret = ret.dropna()
    ret["td"] = ret[fund] - ret[benchmark]

    # Convert to basis points for summary stats
    td_bps = ret["td"] * 1e4
    # Rolling TE as std of TD over window (bps)
    te_bps_series = td_bps.rolling(window=window).std()
    te_bps = float(te_bps_series.dropna().iloc[-1]) if te_bps_series.dropna().size > 0 else None
    td_mean_bps = float(td_bps.rolling(window=window).mean().dropna().iloc[-1]) if td_bps.rolling(window=window).mean().dropna().size > 0 else None

    return ret, td_mean_bps, te_bps
