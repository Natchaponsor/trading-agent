# Trading Agent

Finds Nasdaq-100 stocks in the 2 strongest sectors each week, then alerts your phone and email when a pick reaches its buy zone, sell target or stop loss. You place every trade yourself.

## The team

| Role | Kind | When | Output |
|---|---|---|---|
| 1. Sector Rotation | Claude agent (Opus) + script | Weekly | 2 sectors |
| 2. Technical Finder | Claude agent (Sonnet) + script | Weekly | 1 stock per sector from RSI, MACD, trend, Fibonacci |
| 3. Qualitative Finder | Claude agent (Sonnet) + script + web search | Weekly | 1 stock per sector from growth, earnings, news |
| 4. Stock Picker | Claude agent (Opus) | Weekly | Final picks with buy zone, target, stop |
| 5. Price Alert | Script only, runs on GitHub | Once near the open, once near the close (3 tries each) | Push and email alerts |
| 6. Feedback | Claude agent (Opus) + script | Weekly | Suggested changes you approve |

Scripts do all math. Agents read the numbers, add judgment and news, and explain.

## One-time setup (about 30 minutes)

1. **Put the folder** at `~/Trading Agent` and open Terminal there:
   ```
   cd ~/"Trading Agent"
   python3 -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt
   python -m pytest -q          # should say 12 passed
   ```
2. **Phone alerts:** install the free ntfy app (iPhone or Android), tap +, and subscribe to a long random topic name.
3. **Email alerts (optional):** use a Gmail account as the sender. Turn on 2-step verification, then create an "App password" in Google account settings. Microsoft has been shutting off simple password sign-in for Hotmail and Outlook.com in third-party apps, so sending *from* Hotmail is unreliable. Receiving at Hotmail is fine.
4. `cp .env.example .env` and fill it in. Then test: `python scripts/notify.py --test`
5. **Try the data:** `python scripts/sector_scan.py`. You should see sectors ranked.
6. **GitHub (for daily alerts):** create a **private** repo, then:
   ```
   git init && git add . && git commit -m "Initial Trading Agent"
   git branch -M main
   git remote add origin https://github.com/<you>/trading-agent.git
   git push -u origin main
   ```
   In the repo: Settings > Secrets and variables > Actions, add NTFY_TOPIC, SMTP_HOST, SMTP_PORT, SMTP_USER, SMTP_PASSWORD, ALERT_EMAIL_TO. Then Actions tab > Daily price alerts > Run workflow to test.

## Every Sunday (about 15 minutes)

In the folder, run `claude`, then:
1. `/weekly-review`  (skip the first few weeks until there is history). Approve or reject suggested changes.
2. `/weekly-run`  Claude runs the whole chain and shows you the picks.
3. Say yes to push, so the daily alerts watch the new picks.

On trading days the open check runs between 9:35 AM and 12:00 PM New York time, and the close check between 3:00 and 5:30 PM (GitHub can start runs late, so each gets 3 tries). After you trade, add a row to `data/my_trades.csv` so the feedback agent can compare your real results with the picks.

## Honest limits

- **Paper trade first.** Run it 1-2 months, track picks without real money, and check `data/performance.json` before trusting it.
- **About 20 closed picks** are needed before results mean much. Before that, wins and losses are mostly luck.
- **The Nasdaq-100 is about half tech** (48 of 101 stocks), and only 6 sectors have 3 or more members. Technology will be picked often. Widening to more Nasdaq stocks is a good later upgrade.
- **yfinance is a free, unofficial source.** Prices can be a few minutes late and it occasionally breaks after Yahoo changes. If alerts stop, update it with `pip install -U yfinance`.
- **GitHub schedules can run 5-20 minutes late.** Fine for these checks, not for fast trading.
- This is a research tool for your own decisions, not financial advice.

## Folder map

```
.claude/agents/      the 5 Claude agents
.claude/commands/    /weekly-run and /weekly-review
config/strategy.json all settings the feedback loop can tune (with change log)
config/sectors.json  sector -> benchmark fund
scripts/             data, indicators, alerts, performance (all the math)
tests/               checks that the math is right
data/                picks, reports, alert log, performance
.github/workflows/   daily alert schedule
```
