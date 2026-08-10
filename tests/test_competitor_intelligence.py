import json
from pathlib import Path

from scripts.competitor_intelligence import compare_brands, creative_score, market_gaps, normalize_ads


def load_sample():
    return json.loads(Path("examples/competitor_ads.json").read_text())


def test_normalization_preserves_evidence_boundary():
    rows = normalize_ads(load_sample())
    assert len(rows) == 2
    assert all(row["evidence"] == "Observed" for row in rows)


def test_creative_score_is_not_performance_score():
    result = creative_score(load_sample()[0])
    assert 0 <= result["observable_creative_completeness"] <= 10
    assert "not an estimate of ROAS" in result["warning"]


def test_compare_brands():
    result = compare_brands(load_sample())
    assert set(result) == {"Competitor A", "Competitor B"}
    assert result["Competitor A"]["ad_count_observed"] == 1


def test_market_gap_is_hypothesis():
    gaps = market_gaps(load_sample())
    assert gaps
    # Gaps are structured records, and every one must stay framed as an
    # untested hypothesis rather than an established market fact.
    assert all(gap["type"] == "test_hypothesis" for gap in gaps)
    assert all(gap["caveat"] for gap in gaps)
