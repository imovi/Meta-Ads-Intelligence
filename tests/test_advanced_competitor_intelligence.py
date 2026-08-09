import json
from pathlib import Path

from scripts.competitor_intelligence import competitor_report, recurring_patterns


def load_rows():
    return json.loads(Path("examples/competitor_research.json").read_text())


def test_competitor_report_compares_brands():
    result = competitor_report(load_rows())
    assert result["summary"]["total_ads"] == 4
    assert "Competitor A" in result["brand_comparison"]
    assert result["brand_comparison"]["Competitor A"]["active_count_observed"] == 2


def test_recurring_patterns_are_observation_based():
    patterns = recurring_patterns(load_rows(), min_count=2)
    assert any(p["field"] == "format" and p["pattern"] == "UGC" for p in patterns)


def test_report_has_private_metric_limits():
    result = competitor_report(load_rows())
    assert any("private spend" in item.lower() for item in result["limitations"])
