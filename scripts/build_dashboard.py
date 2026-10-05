"""Build the static dashboard that GitHub Pages serves from docs/.

Reads only files the other scripts and agents already wrote (no new numbers are
invented here, only arranged and compared):
  data/sectors_selected.json, data/sector_scan.json, data/technical_scan.json,
  data/qualitative_data.json, data/picks.json, data/picks_history.jsonl,
  data/performance.json (if present), data/alert_log.csv (if present)

Each build saves a trimmed copy of this week's inputs to
data/weekly/<week_of>/dashboard_data.json, then rebuilds a page for every week
that has one. That is what lets the dashboard look up past weeks after the
main data files are overwritten by a new run.

Writes docs/index.html (latest week) and docs/weeks/<week_of>.html (every week).
Run:  python scripts/build_dashboard.py
"""
from __future__ import annotations

import csv
import html
import json
import sys
from pathlib import Path

from common import DATA, ROOT, load_json, load_strategy

REPO_URL = "https://github.com/Natchaponsor/trading-agent"
REPORTS = [("1_sectors.md", "Sectors"), ("2_technical.md", "Technical"),
           ("3_qualitative.md", "Qualitative"), ("4_picks.md", "Final picks")]


# ---------- small helpers ----------
def esc(x) -> str:
    return html.escape("" if x is None else str(x))


def num(x, digits: int = 2, suffix: str = "", signed: bool = False) -> str:
    if x is None or x == "":
        return '<span class="muted">-</span>'
    try:
        v = float(x)
    except (TypeError, ValueError):
        return esc(x)
    s = f"{v:+.{digits}f}" if signed else f"{v:,.{digits}f}"
    return s + suffix


def signed_cls(x) -> str:
    try:
        return "pos" if float(x) > 0 else "neg" if float(x) < 0 else ""
    except (TypeError, ValueError):
        return ""


def pct(x, digits: int = 1) -> str:
    """Growth fields are fractions (0.25 = 25%)."""
    if x is None:
        return '<span class="muted">-</span>'
    return f'<span class="{signed_cls(x)}">{float(x) * 100:+.{digits}f}%</span>'


def reward_risk(lo, hi, target, stop) -> float | None:
    """Same formula the stock-picker uses: (target - mid) / (mid - stop)."""
    try:
        mid = (float(lo) + float(hi)) / 2
        risk = mid - float(stop)
        return round((float(target) - mid) / risk, 2) if risk > 0 else None
    except (TypeError, ValueError):
        return None


def read_jsonl(path: Path) -> list[dict]:
    if not path.exists():
        return []
    return [json.loads(l) for l in path.read_text().splitlines() if l.strip()]


def read_csv(path: Path) -> list[dict]:
    if not path.exists():
        return []
    with path.open() as f:
        return list(csv.DictReader(f))


# ---------- sections ----------
def picks_section(picks: dict, prices: dict, min_rr: float) -> str:
    items = picks.get("picks", [])
    if not items:
        return '<p class="empty">No stock met the rules this week, so alerts have nothing to watch.</p>'
    cards = []
    for p in items:
        rr = reward_risk(p["entry_low"], p["entry_high"], p["target"], p["stop"])
        price = prices.get(p["ticker"])
        if price is None:
            where = ""
        elif price < p["entry_low"]:
            where = "below the buy zone"
        elif price > p["entry_high"]:
            where = "above the buy zone"
        else:
            where = "inside the buy zone"
        badges = f'<span class="badge">{esc(p.get("source"))}</span>'
        if p.get("exception") or (rr is not None and rr < min_rr):
            badges += f'<span class="badge warn">exception: R/R below {min_rr:g}</span>'
        cards.append(f"""
<article class="pick">
  <header>
    <div><span class="ticker">{esc(p["ticker"])}</span> <span class="muted">{esc(p.get("company"))}</span></div>
    <div class="muted">{esc(p.get("sector"))}</div>
  </header>
  <div class="levels">
    <div><span class="lbl">Buy zone</span><span class="val">{num(p["entry_low"])} to {num(p["entry_high"])}</span></div>
    <div><span class="lbl">Target</span><span class="val pos">{num(p["target"])}</span></div>
    <div><span class="lbl">Stop</span><span class="val neg">{num(p["stop"])}</span></div>
    <div><span class="lbl">Reward to risk</span><span class="val">{num(rr)}</span></div>
  </div>
  <p class="muted small">Last scan price {num(price)}{", " + where if where else ""}.</p>
  <p>{esc(p.get("reason"))}</p>
  <div>{badges}</div>
</article>""")
    return '<div class="cards">' + "".join(cards) + "</div>"


def sectors_section(scan: dict, selected: dict) -> str:
    chosen = set(selected.get("sectors", []))
    rows = []
    for s in sorted(scan.get("sectors", []), key=lambda s: s.get("rank") or 99):
        v = s.get("etf_vs_qqq_pct", {})
        cls = ' class="hl"' if s["sector"] in chosen else ""
        elig = "" if s.get("eligible") else ' <span class="muted small">(too few members)</span>'
        rows.append(f"""<tr{cls}><td>{esc(s.get("rank"))}</td><td>{esc(s["sector"])}{elig}</td><td>{esc(s.get("etf"))}</td>
<td class="r {signed_cls(s.get("score"))}">{num(s.get("score"))}</td>
<td class="r {signed_cls(v.get("1m"))}">{num(v.get("1m"), signed=True)}</td>
<td class="r {signed_cls(v.get("3m"))}">{num(v.get("3m"), signed=True)}</td>
<td class="r {signed_cls(v.get("6m"))}">{num(v.get("6m"), signed=True)}</td>
<td class="r">{esc(s.get("nasdaq100_members"))}</td></tr>""")
    return f"""
<p class="lead">{esc(selected.get("why"))}</p>
<div class="scroll"><table>
<thead><tr><th>#</th><th>Sector</th><th>Fund</th><th class="r">Score</th><th class="r">vs QQQ 1m</th><th class="r">3m</th><th class="r">6m</th><th class="r">Members</th></tr></thead>
<tbody>{"".join(rows)}</tbody></table></div>
<p class="muted small">{esc(scan.get("how_to_read"))} Highlighted rows are this week's sectors.</p>"""


def market_section(scan: dict) -> str:
    rows = []
    for sym, m in scan.get("market_context", {}).items():
        rows.append(f"""<tr><td>{esc(m.get("name"))} <span class="muted small">{esc(sym)}</span></td>
<td class="r">{num(m.get("last"))}</td>
<td class="r {signed_cls(m.get("change_1m_pct"))}">{num(m.get("change_1m_pct"), signed=True, suffix="%")}</td>
<td class="r {signed_cls(m.get("change_3m_pct"))}">{num(m.get("change_3m_pct"), signed=True, suffix="%")}</td>
<td class="r">{"yes" if m.get("above_200day_avg") else "no"}</td></tr>""")
    return f"""<div class="scroll"><table>
<thead><tr><th>Market</th><th class="r">Last</th><th class="r">1 month</th><th class="r">3 months</th><th class="r">Above 200-day avg</th></tr></thead>
<tbody>{"".join(rows)}</tbody></table></div>"""


def candidates_section(sector: str, tech: dict, qual: dict, pick_tickers: set, min_rr: float) -> str:
    t_rows = []
    for s in tech.get("sectors", {}).get(sector, {}).get("top", []):
        lv = s.get("suggested_levels", {})
        ind = s.get("indicators", {})
        rr = lv.get("reward_risk")
        rr_cls = "pos" if rr is not None and rr >= min_rr else "neg"
        mark = ' class="hl"' if s["ticker"] in pick_tickers else ""
        t_rows.append(f"""<tr{mark}><td><b>{esc(s["ticker"])}</b> <span class="muted small">{esc(s.get("company"))}</span></td>
<td class="r">{num(s.get("score"), 1)}</td><td class="r">{num(ind.get("rsi_14"), 1)}</td>
<td>{esc(s.get("fibonacci", {}).get("trend"))}</td>
<td class="r">{num(lv.get("entry_low"))} to {num(lv.get("entry_high"))}</td>
<td class="r">{num(lv.get("target"))}</td><td class="r">{num(lv.get("stop"))}</td>
<td class="r {rr_cls}">{num(rr)}</td></tr>""")
    q_rows = []
    for s in qual.get("sectors", {}).get(sector, {}).get("ranked", [])[:5]:
        mark = ' class="hl"' if s["ticker"] in pick_tickers else ""
        warn = ' <span class="badge warn">earnings soon</span>' if s.get("earnings_within_avoid_window") else ""
        q_rows.append(f"""<tr{mark}><td><b>{esc(s["ticker"])}</b> <span class="muted small">{esc(s.get("company"))}</span></td>
<td class="r">{num(s.get("numbers_score"), 1)}</td>
<td class="r">{pct(s.get("revenueGrowth"))}</td><td class="r">{pct(s.get("earningsGrowth"))}</td>
<td class="r {signed_cls(s.get("analyst_upside_pct"))}">{num(s.get("analyst_upside_pct"), 1, "%", signed=True)}</td>
<td class="r">{num(s.get("forwardPE"), 1)}</td><td>{esc(s.get("next_earnings"))}{warn}</td></tr>""")
    return f"""
<h3>{esc(sector)}</h3>
<div class="grid2">
<div><h4>By chart (technical score)</h4><div class="scroll"><table>
<thead><tr><th>Stock</th><th class="r">Score</th><th class="r">RSI</th><th>Trend</th><th class="r">Buy zone</th><th class="r">Target</th><th class="r">Stop</th><th class="r">R/R</th></tr></thead>
<tbody>{"".join(t_rows) or '<tr><td colspan="8" class="muted">No data</td></tr>'}</tbody></table></div></div>
<div><h4>By business (numbers score, before news)</h4><div class="scroll"><table>
<thead><tr><th>Stock</th><th class="r">Score</th><th class="r">Revenue</th><th class="r">Earnings</th><th class="r">Analyst upside</th><th class="r">Fwd P/E</th><th>Next earnings</th></tr></thead>
<tbody>{"".join(q_rows) or '<tr><td colspan="7" class="muted">No data</td></tr>'}</tbody></table></div></div>
</div>"""


def history_section(history: list[dict], perf: dict | None, note: bool = True) -> str:
    if not history:
        return '<p class="empty">No past picks yet.</p>'
    results = {}
    for r in (perf or {}).get("picks", []):
        results[(r.get("week_of"), r.get("ticker"))] = r
    rows = []
    for p in reversed(history):
        r = results.get((p.get("week_of"), p.get("ticker")), {})
        res = r.get("result", "pending")
        ret = r.get("return_pct")
        rows.append(f"""<tr><td>{esc(p.get("week_of"))}</td><td><b>{esc(p.get("ticker"))}</b></td><td>{esc(p.get("sector"))}</td>
<td class="r">{num(p.get("entry_low"))} to {num(p.get("entry_high"))}</td><td class="r">{num(p.get("target"))}</td><td class="r">{num(p.get("stop"))}</td>
<td><span class="badge res-{esc(res)}">{esc(res.replace("_", " "))}</span></td>
<td class="r {signed_cls(ret)}">{num(ret, signed=True, suffix="%") if ret is not None else '<span class="muted">-</span>'}</td></tr>""")
    return f"""<div class="scroll"><table>
<thead><tr><th>Week</th><th>Stock</th><th>Sector</th><th class="r">Buy zone</th><th class="r">Target</th><th class="r">Stop</th><th>Result</th><th class="r">Return</th></tr></thead>
<tbody>{"".join(rows)}</tbody></table></div>
{'<p class="muted small">Results come from scripts/performance.py, which runs in the weekly review.</p>' if note else ""}"""


def alerts_section(log: list[dict]) -> str:
    if not log:
        return '<p class="empty">No alerts sent yet.</p>'
    cols = list(log[0].keys())
    head = "".join(f"<th>{esc(c)}</th>" for c in cols)
    body = "".join("<tr>" + "".join(f"<td>{esc(r.get(c))}</td>" for c in cols) + "</tr>" for r in log[-15:][::-1])
    return f'<div class="scroll"><table><thead><tr>{head}</tr></thead><tbody>{body}</tbody></table></div>'


def week_picker(weeks: list[str], current: str, prefix: str) -> str:
    """Dropdown plus older/newer links. weeks is newest first."""
    opts = "".join(f'<option value="{prefix}weeks/{esc(w)}.html"{" selected" if w == current else ""}>Week of {esc(w)}</option>'
                   for w in weeks)
    i = weeks.index(current) if current in weeks else 0
    older = f'<a href="{prefix}weeks/{esc(weeks[i + 1])}.html">&larr; Older</a>' if i + 1 < len(weeks) else '<span class="muted">&larr; Older</span>'
    newer = f'<a href="{prefix}weeks/{esc(weeks[i - 1])}.html">Newer &rarr;</a>' if i > 0 else '<span class="muted">Newer &rarr;</span>'
    return f"""<nav class="weeks" aria-label="Choose a week">{older}
<select aria-label="Week" onchange="location.href=this.value">{opts}</select>{newer}</nav>"""


def week_results_section(week: str, valid_until: str, history: list[dict], perf: dict | None, alerts: list[dict]) -> str:
    rows = [p for p in history if p.get("week_of") == week]
    week_alerts = [a for a in alerts if week <= (a.get("time_et") or "")[:10] <= (valid_until or "9999")]
    hist = history_section(rows, perf, note=False) if rows else '<p class="empty">No picks were made this week.</p>'
    return f"""<h3>Picks</h3>{hist}
<h3>Alerts sent that week</h3>{alerts_section(week_alerts)}"""


# ---------- page ----------
CSS = """
:root{--bg:#f7f7f5;--card:#fff;--ink:#1b1d1f;--muted:#6b7075;--line:#e3e3df;--accent:#2f5bd3;
--pos:#147a3d;--neg:#b42318;--hl:#eef3ff;--warn-bg:#fff4e0;--warn:#8a5300;--badge:#eef0f2}
@media (prefers-color-scheme:dark){:root{--bg:#121416;--card:#1a1d20;--ink:#e8eaec;--muted:#9aa1a8;--line:#2c3136;
--accent:#8fb0ff;--pos:#5fd38d;--neg:#ff8a80;--hl:#1e2a44;--warn-bg:#3a2a10;--warn:#ffc46b;--badge:#262b30}}
*{box-sizing:border-box}
body{margin:0;background:var(--bg);color:var(--ink);font:15px/1.5 -apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,Helvetica,Arial,sans-serif}
main{max-width:1100px;margin:0 auto;padding:24px 16px 64px}
h1{font-size:26px;margin:0 0 4px}h2{font-size:19px;margin:40px 0 12px;padding-top:8px;border-top:1px solid var(--line)}
h3{font-size:17px;margin:24px 0 8px}h4{font-size:13px;margin:8px 0;color:var(--muted);text-transform:uppercase;letter-spacing:.04em}
a{color:var(--accent)}.muted{color:var(--muted)}.small{font-size:13px}.lead{font-size:16px;max-width:75ch}
.pos{color:var(--pos)}.neg{color:var(--neg)}.r{text-align:right;white-space:nowrap}
.top{display:flex;justify-content:space-between;align-items:flex-end;flex-wrap:wrap;gap:8px}
.weeks{display:flex;align-items:center;gap:10px;font-size:14px}.weeks select{font:inherit;padding:6px 8px;border-radius:8px;border:1px solid var(--line);background:var(--card);color:var(--ink)}.past{margin:16px 0 0;padding:10px 14px;border-radius:10px;background:var(--warn-bg);color:var(--warn);font-size:14px}.past a{color:inherit;font-weight:600}
.empty{padding:16px;background:var(--card);border:1px dashed var(--line);border-radius:10px;color:var(--muted)}
.cards{display:grid;grid-template-columns:repeat(auto-fit,minmax(300px,1fr));gap:16px}
.pick{background:var(--card);border:1px solid var(--line);border-radius:12px;padding:16px}
.pick header{display:flex;justify-content:space-between;align-items:baseline;gap:8px;flex-wrap:wrap}
.ticker{font-size:24px;font-weight:700}
.levels{display:grid;grid-template-columns:1fr 1fr;gap:10px;margin:14px 0}
.levels div{display:flex;flex-direction:column}.lbl{font-size:12px;color:var(--muted)}.val{font-size:17px;font-weight:600;font-variant-numeric:tabular-nums}
.badge{display:inline-block;font-size:12px;padding:2px 8px;border-radius:99px;background:var(--badge);margin-right:6px}
.badge.warn{background:var(--warn-bg);color:var(--warn)}
.res-win{color:var(--pos)}.res-loss{color:var(--neg)}
.scroll{overflow-x:auto;background:var(--card);border:1px solid var(--line);border-radius:10px}
table{border-collapse:collapse;width:100%;font-variant-numeric:tabular-nums;font-size:14px}
th,td{padding:8px 10px;border-bottom:1px solid var(--line);text-align:left;vertical-align:top}
th{font-size:12px;color:var(--muted);font-weight:600;white-space:nowrap}
tr:last-child td{border-bottom:0}tr.hl td{background:var(--hl)}
.grid2{display:grid;grid-template-columns:minmax(0,1fr);gap:16px}.grid2>div{min-width:0}
@media (min-width:1000px){.grid2{grid-template-columns:minmax(0,1fr) minmax(0,1fr)}}
.reports a{margin-right:16px}
footer{margin-top:48px;font-size:13px;color:var(--muted)}
"""


SNAPSHOT = "dashboard_data.json"


def snapshot(data_dir: Path) -> dict | None:
    """This week's inputs, trimmed to what the page shows."""
    picks = load_json(data_dir / "picks.json", {}) or {}
    selected = load_json(data_dir / "sectors_selected.json", {}) or {}
    week = picks.get("week_of") or selected.get("week_of")
    if not week:
        return None
    tech = load_json(data_dir / "technical_scan.json", {}) or {}
    qual = load_json(data_dir / "qualitative_data.json", {}) or {}
    chosen = selected.get("sectors", [])
    return {
        "week_of": week,
        "strategy": load_strategy(),
        "picks": picks,
        "sectors_selected": selected,
        "sector_scan": load_json(data_dir / "sector_scan.json", {}) or {},
        "technical_scan": {
            "sectors": {k: v for k, v in tech.get("sectors", {}).items() if k in chosen},
            "all_stocks": {t: {"price": v.get("price")} for t, v in tech.get("all_stocks", {}).items()},
        },
        "qualitative_data": {"sectors": {k: {"ranked": v.get("ranked", [])[:5]}
                                         for k, v in qual.get("sectors", {}).items() if k in chosen}},
    }


def build_page(snap: dict, prefix: str, weeks: list[str], data_dir: Path) -> str:
    strategy = snap["strategy"]
    min_rr = float(strategy["technical"]["min_reward_risk"])
    selected, scan = snap["sectors_selected"], snap["sector_scan"]
    tech, qual, picks = snap["technical_scan"], snap["qualitative_data"], snap["picks"]
    perf = load_json(data_dir / "performance.json")
    history = read_jsonl(data_dir / "picks_history.jsonl")
    alerts = read_csv(data_dir / "alert_log.csv")

    week = snap["week_of"]
    latest = week == weeks[0]
    prices = {t: s.get("price") for t, s in tech.get("all_stocks", {}).items()}
    pick_tickers = {p["ticker"] for p in picks.get("picks", [])}
    candidates = "".join(candidates_section(s, tech, qual, pick_tickers, min_rr) for s in selected.get("sectors", []))
    reports = " ".join(f'<a href="{REPO_URL}/blob/main/data/weekly/{esc(week)}/{f}">{label}</a>'
                       for f, label in REPORTS if (data_dir / "weekly" / week / f).exists())
    banner = "" if latest else (f'<p class="past">You are looking at a past week. '
                                f'<a href="{prefix}index.html">Go to the latest week ({esc(weeks[0])})</a></p>')
    record = f"<h2>Track record, all weeks</h2>\n{history_section(history, perf)}" if latest else ""

    return f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Trading Agent: week of {esc(week)}</title><style>{CSS}</style></head>
<body><main>
<div class="top">
  <div><h1>Trading Agent</h1>
  <div class="muted">Week of {esc(week)} to {esc(picks.get("valid_until"))} · strategy v{esc(strategy.get("version"))} · picks made {esc(picks.get("created"))} New York</div></div>
  {week_picker(weeks, week, prefix)}
</div>
{banner}

<h2>Final picks</h2>
{picks_section(picks, prices, min_rr)}

<h2>Sectors: {esc(", ".join(selected.get("sectors", [])))}</h2>
{sectors_section(scan, selected)}

<h2>Candidates by factor</h2>
<p class="muted small">Top 5 per sector from each scan. Final picks are highlighted. R/R is on the scan's own levels; the rule was at least {min_rr:g}.</p>
{candidates}

<h2>Market backdrop</h2>
{market_section(scan)}

<h2>How this week went</h2>
{week_results_section(week, picks.get("valid_until"), history, perf, alerts)}

{record}

<h2>Full reports</h2>
<p class="reports">{reports or '<span class="muted">None for this week.</span>'}</p>

<footer>Personal research for my own decisions, not financial advice. Prices come from script outputs at scan time and may be stale.
Source: <a href="{REPO_URL}">{REPO_URL.replace("https://", "")}</a></footer>
</main></body></html>
"""


def build(out_dir: Path | None = None, data_dir: Path = DATA) -> Path:
    out = Path(out_dir) if out_dir else ROOT / "docs"
    (out / "weeks").mkdir(parents=True, exist_ok=True)
    (out / ".nojekyll").touch()

    current = snapshot(data_dir)
    if current is None:
        raise SystemExit("No week_of in data/picks.json or data/sectors_selected.json")
    snap_file = data_dir / "weekly" / current["week_of"] / SNAPSHOT
    snap_file.parent.mkdir(parents=True, exist_ok=True)
    snap_file.write_text(json.dumps(current, indent=1) + "\n")

    snaps = {p.parent.name: json.loads(p.read_text()) for p in (data_dir / "weekly").glob(f"*/{SNAPSHOT}")}
    weeks = sorted(snaps, reverse=True)
    for w in weeks:
        (out / "weeks" / f"{w}.html").write_text(build_page(snaps[w], "../", weeks, data_dir))
    (out / "index.html").write_text(build_page(snaps[weeks[0]], "", weeks, data_dir))
    return out / "index.html"


if __name__ == "__main__":
    print(f"Dashboard written to {build()}")
    sys.exit(0)
