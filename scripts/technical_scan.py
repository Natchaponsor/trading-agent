"""Step 2 numbers for the Technical Finder agent.

For every Nasdaq-100 stock in the chosen sectors, calculates trend, RSI, MACD,
strength versus QQQ and Fibonacci levels, then gives each a 0-100 score using
the weights in config/strategy.json. Also suggests a buy zone, target and stop.

Reads:  data/sectors_selected.json   ({"sectors": ["Technology", "Industrials"]})
Output: data/technical_scan.json
Run:    python scripts/technical_scan.py
"""
from __future__ import annotations

from common import DATA, load_json, load_sector_map, load_strategy, load_universe, download_prices, now_ny, r2, save_json
from indicators import fib_levels, macd, pct_return, rsi, sma, suggest_levels
from sector_scan import canonical_sector


def analyze_stock(df, qqq_close, cfg: dict) -> dict | None:
    close = df["Close"].dropna()
    if len(close) < 200:
        return None
    price = float(close.iloc[-1])
    s50, s200 = float(sma(close, 50).iloc[-1]), float(sma(close, 200).iloc[-1])
    rsi_now = float(rsi(close).iloc[-1])
    m = macd(close)
    fib = fib_levels(df, cfg["fib_lookback_days"])
    rel_3m = pct_return(close, 63) - pct_return(qqq_close, 63)

    # each part scored 0 to 1
    trend = ((price > s50) + (s50 > s200) + (price > s200)) / 3
    lo, hi = cfg["rsi_sweet_spot"]
    if lo <= rsi_now <= hi:
        rsi_s = 1.0
    elif lo - 10 <= rsi_now < lo or hi < rsi_now <= hi + 5:
        rsi_s = 0.5
    else:
        rsi_s = 0.0
    macd_s = 0.6 * (m["macd"].iloc[-1] > m["signal"].iloc[-1]) + 0.4 * (m["hist"].iloc[-1] > m["hist"].iloc[-4])
    near = any(abs(price / lvl - 1) <= cfg["fib_near_pct"] for k, lvl in fib["retracements"].items() if k in ("0.382", "0.5", "0.618"))
    fib_s = (1.0 if near else 0.5) if fib["trend"] == "up" else 0.0

    levels = suggest_levels(price, fib)
    return {
        "price": r2(price),
        "parts": {"trend": trend, "rsi": rsi_s, "macd": float(macd_s), "fib_pullback": fib_s},
        "rel_3m": rel_3m,
        "indicators": {
            "rsi_14": r2(rsi_now),
            "macd": r2(m["macd"].iloc[-1]),
            "macd_signal": r2(m["signal"].iloc[-1]),
            "macd_hist_rising": bool(m["hist"].iloc[-1] > m["hist"].iloc[-4]),
            "avg_50day": r2(s50),
            "avg_200day": r2(s200),
            "vs_qqq_3m_pct": r2(rel_3m),
            "change_1m_pct": r2(pct_return(close, 21)),
        },
        "fibonacci": {
            "trend": fib["trend"],
            "swing_high": r2(fib["swing_high"]),
            "swing_low": r2(fib["swing_low"]),
            "retracements": {k: r2(v) for k, v in fib["retracements"].items()},
            "extensions": {k: r2(v) for k, v in fib["extensions"].items()},
        },
        "suggested_levels": {k: r2(v) for k, v in levels.items()},
    }


def score_all(results: dict, weights: dict) -> None:
    """Turn the parts into one 0-100 score. Relative strength is ranked within the group."""
    ranked = sorted(results, key=lambda t: results[t]["rel_3m"])
    n = len(ranked)
    for i, t in enumerate(ranked):
        results[t]["parts"]["relative_strength"] = (i / (n - 1)) if n > 1 else 1.0
    for t, r in results.items():
        r["score"] = round(100 * sum(weights[k] * r["parts"][k] for k in weights) / sum(weights.values()), 1)
        r["parts"] = {k: round(v, 2) for k, v in r["parts"].items()}
        r.pop("rel_3m")


def main():
    strategy = load_strategy()
    cfg = strategy["technical"]
    sel = load_json(DATA / "sectors_selected.json")
    if not sel:
        raise SystemExit("Missing data/sectors_selected.json. Run the sector-rotation agent first.")
    sector_map = load_sector_map()
    universe = load_universe()
    universe["canon"] = universe["sector"].map(lambda s: canonical_sector(s, sector_map))

    out = {"created": now_ny().isoformat(timespec="minutes"), "strategy_version": strategy["version"], "sectors": {}}
    for sector in sel["sectors"]:
        members = universe[universe["canon"] == sector]
        prices = download_prices(set(members["ticker"]) | {"QQQ"})
        qqq = prices["QQQ"]["Close"]
        results = {}
        for _, row in members.iterrows():
            if row["ticker"] in prices:
                a = analyze_stock(prices[row["ticker"]], qqq, cfg)
                if a:
                    a["company"] = row["company"]
                    results[row["ticker"]] = a
        score_all(results, cfg["weights"])
        top = sorted(results.items(), key=lambda kv: kv[1]["score"], reverse=True)
        out["sectors"][sector] = {
            "stocks_checked": len(results),
            "top": [{"ticker": t, **r} for t, r in top[: cfg["top_n_per_sector"]]],
        }
        # compact levels for every stock, so the qualitative agent can price its pick too
        out.setdefault("all_stocks", {}).update({
            t: {"sector": sector, "price": r["price"], "score": r["score"],
                "fibonacci": r["fibonacci"], "suggested_levels": r["suggested_levels"]}
            for t, r in results.items()
        })
        print(f"{sector}: " + ", ".join(f"{t} ({r['score']})" for t, r in top[: cfg["top_n_per_sector"]]))
    save_json(DATA / "technical_scan.json", out)


if __name__ == "__main__":
    main()
