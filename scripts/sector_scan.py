"""Step 1 numbers for the Sector Rotation agent.

Compares each sector against the Nasdaq-100 (QQQ) over 1, 3 and 6 months, two ways:
  - the sector fund (ETF), e.g. XLK for Technology
  - the median Nasdaq-100 stock in that sector
Also records big-picture market numbers (US, global, bonds, fear index).

Output: data/sector_scan.json
Run:    python scripts/sector_scan.py
"""
from __future__ import annotations

import statistics

from common import DATA, load_sector_map, load_strategy, load_universe, download_prices, now_ny, r2, save_json
from indicators import pct_return, sma


def canonical_sector(name: str, sector_map: dict) -> str | None:
    for key, info in sector_map["sectors"].items():
        if name == key or name in info.get("aliases", []):
            return key
    return None


def rank_sectors(prices: dict, universe, sector_map: dict, cfg: dict) -> list[dict]:
    bench = sector_map["benchmark"]
    lb = cfg["lookback_days"]
    w = cfg["weights"]
    mix = cfg["etf_vs_members_weight"]
    bench_ret = {k: pct_return(prices[bench]["Close"], d) for k, d in lb.items()}

    universe = universe.copy()
    universe["canon"] = universe["sector"].map(lambda s: canonical_sector(s, sector_map))
    rows = []
    for sector, info in sector_map["sectors"].items():
        members = universe.loc[universe["canon"] == sector, "ticker"].tolist()
        members = [m for m in members if m in prices]
        etf = info["etf"]
        row = {"sector": sector, "etf": etf, "nasdaq100_members": len(members)}

        etf_rel = {}
        if etf in prices:
            for k, d in lb.items():
                r = pct_return(prices[etf]["Close"], d)
                etf_rel[k] = None if r is None or bench_ret[k] is None else r - bench_ret[k]
            c = prices[etf]["Close"]
            row["etf_above_50day_avg"] = bool(c.iloc[-1] > sma(c, 50).iloc[-1])
        mem_rel = {}
        for k, d in lb.items():
            rets = [pct_return(prices[m]["Close"], d) for m in members]
            rets = [x for x in rets if x is not None]
            mem_rel[k] = statistics.median(rets) - bench_ret[k] if rets and bench_ret[k] is not None else None
        row["etf_vs_qqq_pct"] = {k: r2(v) for k, v in etf_rel.items()}
        row["members_median_vs_qqq_pct"] = {k: r2(v) for k, v in mem_rel.items()}

        def blend(rel):
            vals = [(w[k], rel.get(k)) for k in lb if rel.get(k) is not None]
            tot = sum(x for x, _ in vals)
            return sum(x * v for x, v in vals) / tot if tot else None

        e, m = blend(etf_rel), blend(mem_rel)
        if e is not None and m is not None:
            score = mix["etf"] * e + mix["nasdaq_members"] * m
        else:
            score = e if e is not None else m
        row["score"] = r2(score)
        row["eligible"] = len(members) >= cfg["min_nasdaq100_members"] and score is not None
        rows.append(row)
    rows.sort(key=lambda r: (r["eligible"], r["score"] if r["score"] is not None else -1e9), reverse=True)
    for i, r in enumerate(rows, 1):
        r["rank"] = i
    return rows


def market_context(prices: dict, sector_map: dict) -> dict:
    out = {}
    for t, label in sector_map["market_context"].items():
        if t not in prices:
            continue
        c = prices[t]["Close"]
        out[t] = {
            "name": label,
            "last": r2(c.iloc[-1]),
            "change_1m_pct": r2(pct_return(c, 21)),
            "change_3m_pct": r2(pct_return(c, 63)),
            "above_200day_avg": bool(c.iloc[-1] > sma(c, 200).iloc[-1]) if len(c) >= 200 else None,
        }
    return out


def main():
    strategy = load_strategy()
    cfg = strategy["sector_rotation"]
    sector_map = load_sector_map()
    universe = load_universe()
    tickers = set(universe["ticker"]) | {i["etf"] for i in sector_map["sectors"].values()}
    tickers |= set(sector_map["market_context"]) | {sector_map["benchmark"]}
    prices = download_prices(tickers)

    ranked = rank_sectors(prices, universe, sector_map, cfg)
    result = {
        "created": now_ny().isoformat(timespec="minutes"),
        "strategy_version": strategy["version"],
        "how_to_read": "Positive numbers mean the sector beat the Nasdaq-100 (QQQ) by that many percentage points.",
        "market_context": market_context(prices, sector_map),
        "sectors": ranked,
        "suggested_top_sectors": [r["sector"] for r in ranked if r["eligible"]][: cfg["num_sectors"]],
    }
    save_json(DATA / "sector_scan.json", result)
    print("Top sectors by numbers:", ", ".join(result["suggested_top_sectors"]))
    for r in ranked:
        print(f"  {r['rank']:>2}. {r['sector']:<24} score {r['score']}  members {r['nasdaq100_members']}")


if __name__ == "__main__":
    main()
