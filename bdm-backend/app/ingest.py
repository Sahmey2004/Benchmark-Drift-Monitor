
import asyncio
from datetime import date, timedelta
import pandas as pd
import yfinance as yf
from sqlalchemy import select, and_
from sqlalchemy.ext.asyncio import AsyncSession
from .models import Price

async def upsert_prices(db: AsyncSession, df: pd.DataFrame, symbol: str):
    # df index must be DatetimeIndex
    for d, row in df.iterrows():
        pr = Price(symbol=symbol, date=d.date(), adj_close=float(row["Adj Close"]))
        # naive: let duplicates be ignored by unique (not set here) — demo only
        db.add(pr)
    await db.commit()

async def ingest_symbol(db: AsyncSession, symbol: str, days: int = 120):
    end = date.today()
    start = end - timedelta(days=days*2)  # buffer for non-trading days
    data = yf.download(symbol, start=start.isoformat(), end=end.isoformat(), progress=False, auto_adjust=False)
    if data is None or data.empty:
        return 0
    await upsert_prices(db, data, symbol)
    return len(data)

async def ingest_pair(db: AsyncSession, fund: str, benchmark: str, days: int = 120):
    n1 = await ingest_symbol(db, fund, days=days)
    n2 = await ingest_symbol(db, benchmark, days=days)
    return n1 + n2
