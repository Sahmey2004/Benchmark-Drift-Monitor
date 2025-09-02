
import pandas as pd
from app.compute import compute_td_te

def test_compute_td_te_basic():
    dates = pd.date_range("2024-01-01", periods=5, freq="D")
    df = pd.DataFrame({
        "FUND": [100, 101, 102, 103, 104],
        "BM":   [100, 100, 101, 103, 103]
    }, index=dates)
    ret, td_mean_bps, te_bps = compute_td_te(df, "FUND", "BM", window=3)
    assert ret is not None
    assert "td" in ret.columns
    assert td_mean_bps is not None
