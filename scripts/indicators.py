"""Technical indicator math. Pure functions, no internet needed, fully tested."""
from __future__ import annotations

import pandas as pd

FIB_RATIOS = [0.236, 0.382, 0.5, 0.618, 0.786]


def sma(close: pd.Series, n: int) -> pd.Series:
    return close.rolling(n).mean()


def pct_return(close: pd.Series, days: int) -> float | None:
    """Percent change over the last `days` trading days."""
    close = close.dropna()
    if len(close) <= days:
        return None
    return float(close.iloc[-1] / close.iloc[-1 - days] - 1) * 100


def rsi(close: pd.Series, period: int = 14) -> pd.Series:
    """Relative Strength Index (Wilder's smoothing). 0-100."""
    delta = close.diff()
    gain = delta.clip(lower=0)
    loss = -delta.clip(upper=0)
    avg_gain = gain.ewm(alpha=1 / period, min_periods=period, adjust=False).mean()
    avg_loss = loss.ewm(alpha=1 / period, min_periods=period, adjust=False).mean()
    rs = avg_gain / avg_loss
    out = 100 - 100 / (1 + rs)
    out[(avg_loss == 0) & avg_gain.notna()] = 100.0
    return out


def macd(close: pd.Series, fast: int = 12, slow: int = 26, signal: int = 9) -> pd.DataFrame:
    """MACD line, signal line, histogram."""
    line = close.ewm(span=fast, adjust=False).mean() - close.ewm(span=slow, adjust=False).mean()
    sig = line.ewm(span=signal, adjust=False).mean()
    return pd.DataFrame({"macd": line, "signal": sig, "hist": line - sig})


def fib_levels(df: pd.DataFrame, lookback: int = 126) -> dict:
    """Fibonacci retracement and extension levels from the recent swing high and low.

    Uptrend (low came before high): retracements are pullback support levels
    below the high; extensions are profit targets above the high.
    """
    d = df.tail(lookback)
    hi, lo = float(d["High"].max()), float(d["Low"].min())
    uptrend = d["Low"].idxmin() < d["High"].idxmax()
    rng = hi - lo
    if uptrend:
        retr = {str(r): hi - rng * r for r in FIB_RATIOS}
        ext = {"1.272": hi + rng * 0.272, "1.618": hi + rng * 0.618}
    else:
        retr = {str(r): lo + rng * r for r in FIB_RATIOS}
        ext = {"1.272": lo - rng * 0.272, "1.618": lo - rng * 0.618}
    return {
        "trend": "up" if uptrend else "down",
        "swing_high": hi,
        "swing_low": lo,
        "retracements": retr,
        "extensions": ext,
    }


def suggest_levels(price: float, fib: dict, min_gap: float = 0.03) -> dict:
    """Suggest a buy zone, sell target and stop loss from Fibonacci levels.

    Buy zone: nearest support below the price up to the current price.
    Stop: the next support below the buy zone (or the swing low), minus 1%.
    Target: first level at least `min_gap` above the price (swing high, then extensions).
    """
    supports = sorted([v for v in fib["retracements"].values() if v < price], reverse=True)
    entry_low = supports[0] if supports else price * 0.97
    entry_high = price
    lower = [s for s in supports[1:]] + [fib["swing_low"]]
    lower = [s for s in lower if s < entry_low * 0.99]
    stop = (lower[0] if lower else entry_low * 0.95) * 0.99
    candidates = sorted(
        [fib["swing_high"], *fib["extensions"].values(), *fib["retracements"].values()]
    )
    above = [c for c in candidates if c >= price * (1 + min_gap)]
    target = above[0] if above else price * 1.10
    mid = (entry_low + entry_high) / 2
    risk = mid - stop
    reward_risk = (target - mid) / risk if risk > 0 else None
    return {
        "entry_low": entry_low,
        "entry_high": entry_high,
        "target": target,
        "stop": stop,
        "reward_risk": reward_risk,
    }
