import json
from pathlib import Path

from scripts.winning_creatives import detect_winners, group_pattern


def load_rows():
    return json.loads(Path("examples/winning_creatives.json").read_text())


def test_winner_requires_evidence():
    result = detect_winners(load_rows(), min_spend=100, min_conversions=5)
    assert result["qualified_ad_count"] == 3
    assert result["top_ads"][0]["id"] == "ad_001"


def test_repeatable_pattern_is_grouped():
    patterns = group_pattern(load_rows()[:2], "hook_type", min_spend=100, min_conversions=5)
    assert patterns[0]["pattern"] == "problem"
    assert patterns[0]["evidence_strength"] == "sufficient"
    assert patterns[0]["ad_count"] == 2


def test_small_sample_is_excluded_from_qualified_winners():
    result = detect_winners(load_rows(), min_spend=100, min_conversions=5)
    assert all(row["id"] != "ad_004" for row in result["top_ads"])
