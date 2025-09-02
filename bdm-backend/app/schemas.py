
from pydantic import BaseModel
from datetime import date
from typing import List, Optional

class PriceIn(BaseModel):
    symbol: str
    date: date
    adj_close: float

class PriceOut(PriceIn):
    id: int

class MetricPoint(BaseModel):
    date: date
    fund_ret: float
    bench_ret: float
    td: float

class MetricsSummary(BaseModel):
    window: int
    td_mean_bps: float
    te_bps: float
    count: int

class AlertState(BaseModel):
    td_breach: bool
    te_breach: bool
    td_threshold_bps: int
    te_threshold_bps: int
    window: int
    latest_td_bps: Optional[float] = None

class SeriesResponse(BaseModel):
    points: List[MetricPoint]
