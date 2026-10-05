import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))

from build_dashboard import build, reward_risk  # noqa: E402


def test_reward_risk_matches_picker_formula():
    # NVDA week of 2026-10-05: mid 228.29, risk 17.23, reward 27.17
    assert reward_risk(222.63, 233.95, 255.46, 211.06) == 1.58
    assert reward_risk(10, 10, 12, 10) is None  # no risk means no ratio


def test_build_writes_index_and_week(tmp_path):
    index = build(tmp_path)
    html = index.read_text()
    assert html.startswith("<!doctype html>")
    assert "Final picks" in html
    assert list((tmp_path / "weeks").glob("*.html"))
