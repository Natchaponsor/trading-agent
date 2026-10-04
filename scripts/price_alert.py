"""Price Alert (runs twice each trading day, no AI needed).

Checks this week's picks against the live price and sends a push/email when:
  - the price is inside the buy zone            -> "BUY ZONE"
  - the price reached the sell target           -> "SELL: target hit"
  - the price fell to the stop loss             -> "SELL: stop hit"
Each event is sent once per pick. Near the close it also sends a short summary.

Run:  python scripts/price_alert.py            (only acts inside the open/close windows)
      python scripts/price_alert.py --force    (run now, for testing)
"""
from __future__ import annotations

import csv
import datetime as dt
import sys

from common import DATA, load_json, load_strategy, now_ny, save_json
from notify import send

STATE = DATA / "alert_state.json"
LOG = DATA / "alert_log.csv"


def which_session(now: dt.datetime, cfg: dict) -> str | None:
    t = now.strftime("%H:%M")
    if cfg["open_window_et"][0] <= t <= cfg["open_window_et"][1]:
        return "open"
    if cfg["close_window_et"][0] <= t <= cfg["close_window_et"][1]:
        return "close"
    return None


def evaluate_pick(p: dict, price: float, already: set) -> list[tuple[str, str, bool]]:
    """Return new events as (event_name, message, urgent)."""
    t = p["ticker"]
    events = []
    if price <= p["stop"] and "stop" not in already:
        events.append(("stop", f"SELL {t}: hit stop loss. Price {price:.2f} <= stop {p['stop']}. If you hold it, consider selling to limit the loss.", True))
    elif price >= p["target"] and "target" not in already:
        events.append(("target", f"SELL {t}: hit target. Price {price:.2f} >= target {p['target']}. If you hold it, consider taking profit.", True))
    elif p["entry_low"] <= price <= p["entry_high"] and "buy_zone" not in already:
        events.append(("buy_zone", f"BUY ZONE {t}: price {price:.2f} is inside {p['entry_low']}-{p['entry_high']}. Target {p['target']}, stop {p['stop']}.", True))
    return events


def latest_prices(tickers: list[str], today: dt.date) -> dict:
    """Most recent 5-minute price for today. Empty if the market is closed (holiday)."""
    import yfinance as yf

    raw = yf.download(tickers, period="1d", interval="5m", auto_adjust=True,
                      group_by="ticker", progress=False, prepost=False)
    out = {}
    for t in tickers:
        try:
            df = raw[t] if hasattr(raw.columns, "levels") else raw
            close = df["Close"].dropna()
            if len(close) and close.index[-1].tz_convert("America/New_York").date() == today:
                out[t] = float(close.iloc[-1])
        except (KeyError, AttributeError):
            pass
    return out


def main() -> int:
    force = "--force" in sys.argv
    cfg = load_strategy()["alerts"]
    now = now_ny()
    session = which_session(now, cfg) or ("manual" if force else None)
    if session is None:
        print(f"{now:%H:%M} New York time is outside the alert windows. Nothing to do.")
        return 0

    state = load_json(STATE, {"alerted": {}, "last_run": {}})
    run_key = f"{now:%Y-%m-%d}:{session}"
    if not force and state["last_run"].get(session) == f"{now:%Y-%m-%d}":
        print(f"Already ran {run_key}.")
        return 0

    picks = load_json(DATA / "picks.json", {})
    active = [p for p in picks.get("picks", []) if picks.get("valid_until", "9999") >= f"{now:%Y-%m-%d}"]
    if not active:
        print("No active picks this week.")
        return 0

    prices = latest_prices([p["ticker"] for p in active], now.date())
    if not prices:
        print("No prices for today. Market is probably closed (holiday).")
        return 0

    new_log_rows, summary = [], []
    for p in active:
        price = prices.get(p["ticker"])
        if price is None:
            continue
        key = f"{picks['week_of']}:{p['ticker']}"
        already = set(state["alerted"].get(key, []))
        for name, msg, urgent in evaluate_pick(p, price, already):
            send(f"Trading Agent: {p['ticker']} {name.replace('_', ' ')}", msg, urgent)
            print(msg)
            state["alerted"].setdefault(key, []).append(name)
            new_log_rows.append([now.isoformat(timespec="minutes"), session, p["ticker"], name, round(price, 2), p["entry_low"], p["entry_high"], p["target"], p["stop"]])
        summary.append(f"{p['ticker']}: {price:.2f} (buy {p['entry_low']}-{p['entry_high']}, target {p['target']}, stop {p['stop']})")

    if session == "close" and cfg.get("send_close_summary") and summary:
        send("Trading Agent: closing check", "\n".join(summary))

    LOG.parent.mkdir(parents=True, exist_ok=True)
    new_file = not LOG.exists()
    with LOG.open("a", newline="") as f:
        w = csv.writer(f)
        if new_file:
            w.writerow(["time_et", "session", "ticker", "event", "price", "entry_low", "entry_high", "target", "stop"])
        w.writerows(new_log_rows)
    if session in ("open", "close"):
        state["last_run"][session] = f"{now:%Y-%m-%d}"
    save_json(STATE, state)
    print("\n".join(summary))
    return 0


if __name__ == "__main__":
    sys.exit(main())
