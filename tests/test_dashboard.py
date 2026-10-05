import json
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

from build_dashboard import build, reward_risk  # noqa: E402

INPUTS = ["picks.json", "sectors_selected.json", "sector_scan.json", "technical_scan.json", "qualitative_data.json"]


def test_reward_risk_matches_picker_formula():
    # NVDA week of 2026-10-05: mid 228.29, risk 17.23, reward 27.17
    assert reward_risk(222.63, 233.95, 255.46, 211.06) == 1.58
    assert reward_risk(10, 10, 12, 10) is None  # no risk means no ratio


def _fake_data(tmp_path: Path, week: str) -> Path:
    data = tmp_path / "data"
    (data / "weekly").mkdir(parents=True)
    picks = {"week_of": week, "valid_until": week, "created": f"{week}T09:00",
             "picks": [{"ticker": "AAA", "company": "A Co", "sector": "Tech", "entry_low": 9, "entry_high": 10,
                        "target": 14, "stop": 8, "source": "technical", "reason": "test"}]}
    (data / "picks.json").write_text(json.dumps(picks))
    (data / "sectors_selected.json").write_text(json.dumps({"week_of": week, "sectors": ["Tech"], "why": "test"}))
    return data


def test_each_week_gets_a_page_and_past_weeks_stay(tmp_path):
    data = _fake_data(tmp_path, "2026-01-05")
    out = tmp_path / "docs"
    build(out, data)
    # next week's run overwrites the main data files
    (data / "picks.json").write_text((data / "picks.json").read_text().replace("2026-01-05", "2026-01-12").replace("AAA", "BBB"))
    (data / "sectors_selected.json").write_text((data / "sectors_selected.json").read_text().replace("2026-01-05", "2026-01-12"))
    index = build(out, data).read_text()

    old = (out / "weeks" / "2026-01-05.html").read_text()
    assert "Week of 2026-01-12" in index and "BBB" in index
    assert "AAA" in old and "BBB" not in old.split("<h2>Final picks</h2>")[1].split("<h2>")[0]
    assert "past week" in old and "past week" not in index
    assert 'weeks/2026-01-05.html' in index  # picker lists the older week


def test_build_from_real_data(tmp_path):
    data = tmp_path / "data"
    (data / "weekly").mkdir(parents=True)
    for f in INPUTS:
        if (ROOT / "data" / f).exists():
            shutil.copy(ROOT / "data" / f, data / f)
    html = build(tmp_path / "docs", data).read_text()
    assert html.startswith("<!doctype html>")
    assert "Final picks" in html
