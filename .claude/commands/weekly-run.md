---
description: Run the weekly stock-finding chain (sectors, technical, qualitative, final picks)
---
Run the weekly pipeline for the coming week. Work through these steps in order and tell me briefly when each finishes.

1. Work out week_of (the coming Monday, New York date) and create data/weekly/<week_of>/.
2. Run `python scripts/sector_scan.py`.
3. Use the sector-rotation agent. Wait for data/sectors_selected.json.
4. Run `python scripts/technical_scan.py` and `python scripts/qualitative_data.py`.
5. Use the technical-finder agent and the qualitative-finder agent at the same time (in parallel). Wait for both reports.
6. Use the stock-picker agent. It must finish with validate_picks.py reporting the picks are valid.
7. Show me: the 2 sectors and why, then a table of the final picks (ticker, buy zone, target, stop, reward to risk, source) and one line on each.
8. Ask me whether to commit and push data/ so the daily alerts on GitHub use the new picks. Only push after I say yes.

If any script fails, stop and show me the error. Never fill in prices yourself.
