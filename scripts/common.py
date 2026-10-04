"""Shared helpers: paths, config, stock list, price download, small file utils."""
from __future__ import annotations

import datetime as dt
import io
import json
import pickle
import time
from pathlib import Path
from zoneinfo import ZoneInfo

import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data"
CONFIG = ROOT / "config"
CACHE = DATA / "cache"
NY = ZoneInfo("America/New_York")

try:  # load .env if present (local runs); GitHub Actions uses secrets instead
    from dotenv import load_dotenv

    load_dotenv(ROOT / ".env")
except ImportError:
    pass


# ---------- small file helpers ----------
def load_json(path, default=None):
    p = Path(path)
    if not p.exists():
        return default
    return json.loads(p.read_text())


def save_json(path, obj) -> None:
    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(obj, indent=2, default=_json_default))


def _json_default(o):
    if hasattr(o, "item"):  # numpy numbers
        return o.item()
    if isinstance(o, (dt.date, dt.datetime, pd.Timestamp)):
        return o.isoformat()
    return str(o)


def load_strategy() -> dict:
    return load_json(CONFIG / "strategy.json")


def load_sector_map() -> dict:
    return load_json(CONFIG / "sectors.json")


def now_ny() -> dt.datetime:
    return dt.datetime.now(NY)


def r2(x):
    """Round to 2 decimals, keep None."""
    return None if x is None or pd.isna(x) else round(float(x), 2)


# ---------- Nasdaq-100 stock list ----------
UNIVERSE_CACHE = CONFIG / "universe_nasdaq100.csv"
WIKI_URL = "https://en.wikipedia.org/wiki/Nasdaq-100"


def load_universe(refresh: bool = False) -> pd.DataFrame:
    """Return a table with columns: ticker, company, sector.

    Pulled from the Nasdaq-100 table on Wikipedia and saved for 30 days.
    Sector names there use the ICB system (Technology, Health Care, ...).
    """
    if UNIVERSE_CACHE.exists() and not refresh:
        age_days = (time.time() - UNIVERSE_CACHE.stat().st_mtime) / 86400
        if age_days < 30:
            return pd.read_csv(UNIVERSE_CACHE)
    try:
        import requests

        html = requests.get(
            WIKI_URL,
            headers={"User-Agent": "Mozilla/5.0 (personal trading-agent project)"},
            timeout=30,
        ).text
        for t in pd.read_html(io.StringIO(html)):
            cols = {str(c).strip().lower(): c for c in t.columns}
            tick = cols.get("ticker") or cols.get("symbol")
            comp = cols.get("company") or cols.get("security")
            sector = next(
                (cols[c] for c in cols if ("sector" in c or "industry" in c) and "sub" not in c),
                None,
            )
            if tick is not None and sector is not None and len(t) >= 80:
                df = pd.DataFrame(
                    {
                        "ticker": t[tick].astype(str).str.strip().str.replace(".", "-", regex=False),
                        "company": t[comp] if comp is not None else "",
                        "sector": t[sector].astype(str).str.strip(),
                    }
                )
                UNIVERSE_CACHE.parent.mkdir(parents=True, exist_ok=True)
                df.to_csv(UNIVERSE_CACHE, index=False)
                return df
        raise ValueError("Nasdaq-100 table not found on the Wikipedia page")
    except Exception as e:  # network or page-format problem
        if UNIVERSE_CACHE.exists():
            print(f"Warning: could not refresh stock list ({e}). Using saved list.")
            return pd.read_csv(UNIVERSE_CACHE)
        raise


# ---------- price data ----------
def download_prices(tickers, period: str = "1y", interval: str = "1d", use_cache: bool = True) -> dict:
    """Download daily price history. Returns {ticker: DataFrame(Open, High, Low, Close, Volume)}.

    Results are cached per day so the weekly run only downloads once.
    """
    import yfinance as yf

    tickers = sorted(set(tickers))
    cache_file = CACHE / f"prices_{period}_{interval}_{now_ny():%Y-%m-%d}.pkl"
    cached: dict = {}
    if use_cache and cache_file.exists():
        cached = pickle.loads(cache_file.read_bytes())
    missing = [t for t in tickers if t not in cached]
    if missing:
        raw = yf.download(
            missing, period=period, interval=interval, auto_adjust=True,
            group_by="ticker", progress=False, threads=True,
        )
        for t in missing:
            try:
                df = raw[t] if isinstance(raw.columns, pd.MultiIndex) else raw
                df = df.dropna(how="all")
                if len(df):
                    cached[t] = df
                else:
                    print(f"Warning: no price data for {t}")
            except KeyError:
                print(f"Warning: no price data for {t}")
        if use_cache:
            CACHE.mkdir(parents=True, exist_ok=True)
            cache_file.write_bytes(pickle.dumps(cached))
    return {t: cached[t] for t in tickers if t in cached}
