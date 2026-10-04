"""Step 2 numbers for the Qualitative Finder agent.

For every Nasdaq-100 stock in the chosen sectors, pulls growth, profit, valuation,
analyst price targets and the next earnings date, then gives a starting 0-100
score. The agent adds news and judgment on top (it reads news with web search).

Reads:  data/sectors_selected.json
Output: data/qualitative_data.json
Run:    python scripts/qualitative_data.py
"""
from __future__ import annotations

import datetime as dt

from common import DATA, load_json, load_sector_map, load_strategy, load_universe, now_ny, r2, save_json
from sector_scan import canonical_sector

FIELDS = [
    "marketCap", "revenueGrowth", "earningsGrowth", "profitMargins", "forwardPE",
    "trailingPE", "pegRatio", "targetMeanPrice", "recommendationMean",
    "numberOfAnalystOpinions", "currentPrice",
]


def next_earnings_date(tk) -> str | None:
    try:
        cal = tk.calendar
        dates = cal.get("Earnings Date") if isinstance(cal, dict) else None
        if dates:
            return str(min(dates))
    except Exception:
        pass
    return None


def fetch_one(ticker: str) -> dict:
    import yfinance as yf

    tk = yf.Ticker(ticker)
    try:
        info = tk.info or {}
    except Exception as e:
        return {"error": str(e)}
    d = {k: info.get(k) for k in FIELDS}
    price, target = d.get("currentPrice"), d.get("targetMeanPrice")
    d["analyst_upside_pct"] = r2((target / price - 1) * 100) if price and target else None
    d["next_earnings"] = next_earnings_date(tk)
    return d


def clamp01(x):
    return max(0.0, min(1.0, x))


def base_score(d: dict, weights: dict) -> float | None:
    """Score from numbers only. 'news' weight is left for the agent to fill in."""
    parts = {}
    if d.get("revenueGrowth") is not None:
        parts["revenue_growth"] = clamp01(d["revenueGrowth"] / 0.30)  # 30%+ growth = full marks
    if d.get("earningsGrowth") is not None:
        parts["earnings_growth"] = clamp01(d["earningsGrowth"] / 0.40)  # 40%+ = full marks
    if d.get("analyst_upside_pct") is not None:
        parts["analyst_upside"] = clamp01(d["analyst_upside_pct"] / 25)  # 25%+ upside = full marks
    if not parts:
        return None
    tot = sum(weights[k] for k in parts)
    return round(100 * sum(weights[k] * v for k, v in parts.items()) / tot, 1)


def main():
    strategy = load_strategy()
    cfg = strategy["qualitative"]
    sel = load_json(DATA / "sectors_selected.json")
    if not sel:
        raise SystemExit("Missing data/sectors_selected.json. Run the sector-rotation agent first.")
    sector_map = load_sector_map()
    universe = load_universe()
    universe["canon"] = universe["sector"].map(lambda s: canonical_sector(s, sector_map))
    today = now_ny().date()

    out = {"created": now_ny().isoformat(timespec="minutes"), "strategy_version": strategy["version"],
           "note": "Growth numbers are year-over-year (0.25 = 25%). numbers_score excludes news; the agent adds that.",
           "sectors": {}}
    for sector in sel["sectors"]:
        rows = []
        for _, row in universe[universe["canon"] == sector].iterrows():
            d = fetch_one(row["ticker"])
            d["ticker"], d["company"] = row["ticker"], row["company"]
            d["numbers_score"] = base_score(d, cfg["weights"])
            if d.get("next_earnings"):
                try:
                    days = (dt.date.fromisoformat(d["next_earnings"][:10]) - today).days
                    d["earnings_within_avoid_window"] = 0 <= days <= cfg["avoid_earnings_within_days"]
                except ValueError:
                    pass
            rows.append(d)
        rows.sort(key=lambda d: d["numbers_score"] or -1, reverse=True)
        out["sectors"][sector] = {"stocks_checked": len(rows), "ranked": rows}
        print(f"{sector}: " + ", ".join(f"{d['ticker']} ({d['numbers_score']})" for d in rows[:5]))
    save_json(DATA / "qualitative_data.json", out)


if __name__ == "__main__":
    main()
