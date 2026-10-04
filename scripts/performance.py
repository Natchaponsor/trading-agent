"""Score every past pick so the Feedback agent works from facts, not memory.

For each pick in data/picks_history.jsonl, looks at daily prices after the pick:
  never_entered  price never reached the buy zone while the pick was valid
  win            after entering, the target was hit before the stop
  loss           after entering, the stop was hit first
  open           entered, neither level hit yet
  timed_out      entered, neither hit within the max holding period (exit at last close)
Compares each result with QQQ over the same days.

Also reads data/my_trades.csv (your real trades) if you keep it.
Output: data/performance.json
Run:    python scripts/performance.py
"""
from __future__ import annotations

import json
import statistics

import pandas as pd

from common import DATA, download_prices, load_strategy, now_ny, r2, save_json


def evaluate_pick(p: dict, daily: pd.DataFrame, max_days: int) -> dict:
    """daily: prices from the pick's first trading day onward."""
    valid = daily[daily.index.strftime("%Y-%m-%d") <= p["valid_until"]]
    entered = valid[(valid["Low"] <= p["entry_high"]) & (valid["High"] >= p["entry_low"])]
    if entered.empty:
        return {"result": "never_entered"}
    entry_day = entered.index[0]
    entry_price = (p["entry_low"] + p["entry_high"]) / 2
    after = daily[daily.index >= entry_day].head(max_days)
    for day, row in after.iterrows():
        hit_stop, hit_target = row["Low"] <= p["stop"], row["High"] >= p["target"]
        if hit_stop:  # if both on one day, assume the worse case
            return {"result": "loss", "entry_day": str(entry_day.date()), "exit_day": str(day.date()),
                    "return_pct": r2((p["stop"] / entry_price - 1) * 100)}
        if hit_target:
            return {"result": "win", "entry_day": str(entry_day.date()), "exit_day": str(day.date()),
                    "return_pct": r2((p["target"] / entry_price - 1) * 100)}
    last = float(after["Close"].iloc[-1])
    status = "timed_out" if len(after) >= max_days else "open"
    return {"result": status, "entry_day": str(entry_day.date()), "exit_day": str(after.index[-1].date()),
            "return_pct": r2((last / entry_price - 1) * 100)}


def summarize(rows: list[dict]) -> dict:
    done = [r for r in rows if r["result"] in ("win", "loss", "timed_out")]
    def stats(group):
        rets = [r["return_pct"] for r in group if r.get("return_pct") is not None]
        vs = [r["vs_qqq_pct"] for r in group if r.get("vs_qqq_pct") is not None]
        return {
            "closed_picks": len(group),
            "win_rate_pct": r2(100 * sum(r["result"] == "win" for r in group) / len(group)) if group else None,
            "avg_return_pct": r2(statistics.mean(rets)) if rets else None,
            "avg_vs_qqq_pct": r2(statistics.mean(vs)) if vs else None,
        }
    out = {
        "total_picks": len(rows),
        "never_entered": sum(r["result"] == "never_entered" for r in rows),
        "still_open": sum(r["result"] == "open" for r in rows),
        "overall": stats(done),
        "by_source": {s: stats([r for r in done if r.get("source") == s]) for s in ("technical", "qualitative", "both")},
        "by_sector": {s: stats([r for r in done if r["sector"] == s]) for s in sorted({r["sector"] for r in done})},
        "enough_data": len(done) >= 20,
        "warning": None if len(done) >= 20 else f"Only {len(done)} closed picks. Patterns are not reliable until about 20.",
    }
    return out


def main():
    hist = DATA / "picks_history.jsonl"
    if not hist.exists():
        print("No pick history yet.")
        return
    picks = [json.loads(l) for l in hist.read_text().splitlines() if l.strip()]
    max_days = load_strategy()["performance"]["max_holding_trading_days"]
    prices = download_prices({p["ticker"] for p in picks} | {"QQQ"}, period="2y", use_cache=False)

    rows = []
    for p in picks:
        df = prices.get(p["ticker"])
        base = {k: p.get(k) for k in ("week_of", "ticker", "sector", "source", "strategy_version", "entry_low", "entry_high", "target", "stop")}
        if df is None:
            rows.append({**base, "result": "no_data"})
            continue
        daily = df[df.index.strftime("%Y-%m-%d") >= p["week_of"]]
        res = evaluate_pick(p, daily, max_days)
        if res.get("entry_day"):
            q = prices["QQQ"]["Close"]
            q = q[(q.index.strftime("%Y-%m-%d") >= res["entry_day"]) & (q.index.strftime("%Y-%m-%d") <= res["exit_day"])]
            if len(q) > 1:
                res["vs_qqq_pct"] = r2(res["return_pct"] - (q.iloc[-1] / q.iloc[0] - 1) * 100)
        rows.append({**base, **res})

    trades_file = DATA / "my_trades.csv"
    my_trades = pd.read_csv(trades_file).to_dict("records") if trades_file.exists() else []
    save_json(DATA / "performance.json", {
        "created": now_ny().isoformat(timespec="minutes"),
        "summary": summarize(rows),
        "picks": rows,
        "my_trades": my_trades,
    })
    print(json.dumps(summarize(rows), indent=2))


if __name__ == "__main__":
    main()
