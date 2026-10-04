"""Check the Stock Picker's output before alerts use it, then add it to the history.

Catches mistakes like a stop loss above the buy price or a made-up price far from
the real one. Run after the stock-picker agent writes data/picks.json:

    python scripts/validate_picks.py
"""
from __future__ import annotations

import json
import sys

from common import DATA, load_json, load_strategy, load_universe

REQUIRED = ["ticker", "sector", "entry_low", "entry_high", "target", "stop", "source", "reason"]


def check_pick(p: dict, last_price: float | None, max_stop_pct: float) -> list[str]:
    errs = [f"missing '{k}'" for k in REQUIRED if p.get(k) in (None, "")]
    if errs:
        return errs
    lo, hi, tgt, stop = (float(p[k]) for k in ("entry_low", "entry_high", "target", "stop"))
    if not stop < lo <= hi < tgt:
        errs.append(f"levels out of order: need stop {stop} < buy low {lo} <= buy high {hi} < target {tgt}")
    if (hi - stop) / hi * 100 > max_stop_pct:
        errs.append(f"stop is more than {max_stop_pct}% below the buy zone")
    if p["source"] not in ("technical", "qualitative", "both"):
        errs.append("source must be technical, qualitative or both")
    if last_price and not (0.85 * last_price <= hi <= 1.15 * last_price):
        errs.append(f"buy zone {lo}-{hi} is more than 15% away from last price {last_price}")
    return errs


def main() -> int:
    picks = load_json(DATA / "picks.json")
    if not picks:
        print("No data/picks.json found.")
        return 1
    strategy = load_strategy()
    tickers = set(load_universe()["ticker"])
    tech = load_json(DATA / "technical_scan.json", {"sectors": {}})
    last = {t: s["price"] for t, s in tech.get("all_stocks", {}).items()}

    problems = 0
    for p in picks.get("picks", []):
        errs = check_pick(p, last.get(p.get("ticker")), strategy["picker"]["max_stop_distance_pct"])
        if p.get("ticker") not in tickers:
            errs.append("ticker is not in the Nasdaq-100 list")
        print(f"{p.get('ticker')}: {'OK' if not errs else '; '.join(errs)}")
        problems += len(errs)
    if problems:
        print("Fix the problems above before alerts can use these picks.")
        return 1

    hist = DATA / "picks_history.jsonl"
    seen = set()
    if hist.exists():
        seen = {(json.loads(l)["week_of"], json.loads(l)["ticker"]) for l in hist.read_text().splitlines() if l.strip()}
    with hist.open("a") as f:
        for p in picks["picks"]:
            if (picks["week_of"], p["ticker"]) not in seen:
                f.write(json.dumps({"week_of": picks["week_of"], "valid_until": picks["valid_until"],
                                    "strategy_version": strategy["version"], **p}) + "\n")
    print("Picks are valid and saved to history.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
