# Trading Agent

Personal research tool that finds Nasdaq-100 stocks in the 2 strongest sectors each week and alerts me when to buy or sell. I (Top) place all trades myself. Nothing here places orders.

## How it works
Weekly (Sunday, `/weekly-review` then `/weekly-run`):
1. scripts/sector_scan.py -> sector-rotation agent -> data/sectors_selected.json
2. scripts/technical_scan.py + scripts/qualitative_data.py -> technical-finder and qualitative-finder agents (in parallel)
3. stock-picker agent -> data/picks.json -> scripts/validate_picks.py
4. feedback agent (in /weekly-review) -> data/feedback/<date>.md, proposals only

Daily (GitHub Actions, no AI): scripts/price_alert.py checks once in the open window (9:35 AM-12:00 PM New York) and once in the close window (3:00-5:30 PM). Each window gets 3 scheduled tries because GitHub runs late; scripts/alert_gate.py skips the tries after the first one finishes. It sends push/email alerts and logs to data/alert_log.csv.

## Rules for every agent and session
- Code calculates, agents judge. Every price, indicator or return in a report must come from a script output file or a linked source. Never estimate or invent a number.
- Only scripts/indicators.py computes indicators. If a new indicator is needed, add it there with a test in tests/.
- config/strategy.json changes only after I approve, and every change gets a change_log entry and a version bump.
- Never commit .env or put keys in code.
- Reports are short and in plain language (12th-grade level, no jargon, no em dashes).
- This is research for my own decisions, not financial advice.

## Files
- config/strategy.json: all settings and weights (the "model" the feedback loop tunes)
- config/sectors.json: sector names -> sector fund used as benchmark
- config/universe_nasdaq100.csv: saved stock list (refreshed from Wikipedia every 30 days)
- data/weekly/<week_of>/: the 4 reports for that week
- data/picks.json: this week's picks (what alerts watch); data/picks_history.jsonl: all past picks
- data/performance.json, data/feedback/: results and coaching notes
- data/my_trades.csv: my real trades, filled in by me
- docs/: public dashboard (GitHub Pages), built by scripts/build_dashboard.py; never edit by hand
- data/weekly/<week_of>/dashboard_data.json: snapshot of that week's inputs so past weeks stay viewable

## Commands
- Tests: `python -m pytest -q`
- Alert test: `python scripts/notify.py --test`, `python scripts/price_alert.py --force`
