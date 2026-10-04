"""Tests on made-up price data, so they run without internet. Run: python -m pytest -q"""
import datetime as dt
import sys
from pathlib import Path

import numpy as np
import pandas as pd
import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))

from common import NY, load_sector_map, load_strategy  # noqa: E402
from indicators import fib_levels, macd, pct_return, rsi, suggest_levels  # noqa: E402
import price_alert  # noqa: E402
import performance  # noqa: E402
from sector_scan import rank_sectors  # noqa: E402
from technical_scan import analyze_stock, score_all  # noqa: E402
from validate_picks import check_pick  # noqa: E402


def make_prices(start=100, drift=0.001, n=260, seed=0):
    rng = np.random.default_rng(seed)
    close = start * np.cumprod(1 + drift + rng.normal(0, 0.01, n))
    idx = pd.bdate_range("2025-09-01", periods=n)
    return pd.DataFrame({"Open": close, "High": close * 1.01, "Low": close * 0.99, "Close": close, "Volume": 1e6}, index=idx)


def test_rsi_range_and_extremes():
    up = pd.Series(np.arange(1, 60, dtype=float))
    assert rsi(up).iloc[-1] == 100
    r = rsi(make_prices()["Close"]).dropna()
    assert ((r >= 0) & (r <= 100)).all()


def test_rsi_known_value():
    # alternating +1/-1 moves -> equal average gain and loss -> RSI near 50
    s = pd.Series(100 + np.tile([0, 1], 50), dtype=float)
    assert abs(rsi(s).iloc[-1] - 50) < 5


def test_macd_positive_in_uptrend():
    m = macd(pd.Series(np.linspace(100, 200, 100)))
    assert m["macd"].iloc[-1] > 0


def test_pct_return():
    s = pd.Series([100.0, 110.0, 121.0])
    assert pct_return(s, 2) == pytest.approx(21.0)
    assert pct_return(s, 5) is None


def test_fib_uptrend_levels():
    df = pd.DataFrame({"High": [100, 120, 150, 200], "Low": [100, 110, 140, 190], "Close": [100, 115, 145, 195]},
                      index=pd.bdate_range("2026-01-01", periods=4))
    f = fib_levels(df)
    assert f["trend"] == "up"
    assert f["retracements"]["0.5"] == pytest.approx(150)  # halfway between 100 and 200
    assert f["extensions"]["1.618"] == pytest.approx(261.8)


def test_suggested_levels_in_order():
    df = make_prices(drift=0.002)
    f = fib_levels(df)
    price = float(df["Close"].iloc[-1]) * 0.93  # pretend a pullback
    lv = suggest_levels(price, f)
    assert lv["stop"] < lv["entry_low"] <= lv["entry_high"] < lv["target"]


def test_technical_score_prefers_uptrend():
    qqq = make_prices(seed=1)["Close"]
    cfg = load_strategy()["technical"]
    res = {"UP": analyze_stock(make_prices(drift=0.003, seed=2), qqq, cfg),
           "DOWN": analyze_stock(make_prices(drift=-0.003, seed=3), qqq, cfg)}
    score_all(res, cfg["weights"])
    assert res["UP"]["score"] > res["DOWN"]["score"]
    assert 0 <= res["DOWN"]["score"] <= 100


def test_sector_ranking():
    sm = load_sector_map()
    prices = {"QQQ": make_prices(drift=0.001, seed=9)}
    uni = []
    for sector, info in sm["sectors"].items():
        drift = 0.004 if sector == "Energy" else 0.0
        prices[info["etf"]] = make_prices(drift=drift, seed=hash(sector) % 100)
        for i in range(4):
            t = f"{info['etf']}{i}"
            prices[t] = make_prices(drift=drift, seed=i)
            uni.append({"ticker": t, "company": t, "sector": sector})
    ranked = rank_sectors(prices, pd.DataFrame(uni), sm, load_strategy()["sector_rotation"])
    assert ranked[0]["sector"] == "Energy"


PICK = {"ticker": "ABC", "entry_low": 95.0, "entry_high": 100.0, "target": 115.0, "stop": 90.0,
        "sector": "Technology", "source": "technical", "reason": "test"}


def test_alert_events():
    assert price_alert.evaluate_pick(PICK, 97, set())[0][0] == "buy_zone"
    assert price_alert.evaluate_pick(PICK, 97, {"buy_zone"}) == []
    assert price_alert.evaluate_pick(PICK, 116, set())[0][0] == "target"
    assert price_alert.evaluate_pick(PICK, 89, set())[0][0] == "stop"
    assert price_alert.evaluate_pick(PICK, 105, set()) == []


def test_alert_windows():
    cfg = load_strategy()["alerts"]
    at = lambda h, m: dt.datetime(2026, 10, 5, h, m, tzinfo=NY)
    assert price_alert.which_session(at(9, 45), cfg) == "open"
    assert price_alert.which_session(at(10, 45), cfg) is None
    assert price_alert.which_session(at(15, 30), cfg) == "close"
    assert price_alert.which_session(at(16, 30), cfg) is None


def _bars(rows):
    idx = pd.bdate_range("2026-10-05", periods=len(rows))
    return pd.DataFrame(rows, columns=["Low", "High", "Close"], index=idx)


def test_performance_results():
    p = {**PICK, "valid_until": "2026-10-09"}
    assert performance.evaluate_pick(p, _bars([(101, 104, 103)] * 5), 20)["result"] == "never_entered"
    win = performance.evaluate_pick(p, _bars([(96, 101, 99), (100, 116, 115)]), 20)
    assert win["result"] == "win" and win["return_pct"] > 0
    assert performance.evaluate_pick(p, _bars([(96, 101, 99), (89, 99, 90)]), 20)["result"] == "loss"
    assert performance.evaluate_pick(p, _bars([(96, 101, 99), (97, 105, 104)]), 20)["result"] == "open"


def test_validate_pick():
    assert check_pick(PICK, 98, 10) == []
    bad = {**PICK, "stop": 99}
    assert any("order" in e for e in check_pick(bad, 98, 10))
    assert any("15%" in e for e in check_pick(PICK, 150, 10))
