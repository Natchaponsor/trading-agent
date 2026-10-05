"""Decide whether a scheduled alert run should do anything (standard library only).

GitHub can start scheduled runs late or skip them, so each alert window gets 3
tries. The first try that finishes marks the session done in data/alert_state.json
(see price_alert.py), and this gate makes the later tries stop right away, before
installing anything.

Run:  python scripts/alert_gate.py     prints run=true or run=false
      (also writes it to $GITHUB_OUTPUT when running on GitHub Actions)
"""
from __future__ import annotations

import datetime as dt
import json
import os
import sys
from pathlib import Path
from zoneinfo import ZoneInfo

ROOT = Path(__file__).resolve().parent.parent
NY = ZoneInfo("America/New_York")


def which_session(now: dt.datetime, cfg: dict) -> str | None:
    t = now.strftime("%H:%M")
    if cfg["open_window_et"][0] <= t <= cfg["open_window_et"][1]:
        return "open"
    if cfg["close_window_et"][0] <= t <= cfg["close_window_et"][1]:
        return "close"
    return None


def should_run(now: dt.datetime, cfg: dict, state: dict) -> tuple[bool, str]:
    session = which_session(now, cfg)
    if session is None:
        return False, f"{now:%H:%M} New York time is outside the alert windows."
    if state.get("last_run", {}).get(session) == f"{now:%Y-%m-%d}":
        return False, f"The {session} check already ran today. Skipping this try."
    return True, f"Running the {session} check."


def main() -> int:
    cfg = json.loads((ROOT / "config" / "strategy.json").read_text())["alerts"]
    state_file = ROOT / "data" / "alert_state.json"
    state = json.loads(state_file.read_text()) if state_file.exists() else {}
    run, why = should_run(dt.datetime.now(NY), cfg, state)
    print(why)
    print(f"run={'true' if run else 'false'}")
    if os.getenv("GITHUB_OUTPUT"):
        with open(os.environ["GITHUB_OUTPUT"], "a") as f:
            f.write(f"run={'true' if run else 'false'}\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
