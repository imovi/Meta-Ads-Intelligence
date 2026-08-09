import json
from pathlib import Path

from scripts.creative_fatigue import analyze_fatigue, compare_variations


def load_history():
    return json.loads(Path("examples/creative_fatigue_history.json").read_text())


def test_detects_multi_signal_fatigue():
    result = analyze_fatigue(load_history())
    assert result["signal"] is True
    assert result["status"] == "likely_fatigue_signal"
    assert result["confidence"] in {"medium", "high"}


def test_requires_multiple_periods():
    result = analyze_fatigue(load_history()[:2])
    assert result["signal"] is False
    assert result["status"] == "insufficient_data"


def test_variation_evidence_flag():
    result = compare_variations([
        {"id": "a", "spend": 300, "conversions": 20, "roas": 3},
        {"id": "b", "spend": 20, "conversions": 2, "roas": 8},
    ])
    assert result[0]["id"] == "a"
    assert result[1]["evidence_strength"] == "weak"
