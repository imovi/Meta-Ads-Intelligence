from scripts.creative_intelligence import analyze_copy, creative_completeness, fatigue_signal, rank_creatives


def test_copy_analysis():
    row = {
        "hook": "Problem hook",
        "problem": "Pain",
        "solution": "Solution",
        "benefit": "Benefit",
        "proof": "Testimonial",
        "offer": "10% off",
        "cta": "Shop Now",
        "primary_text": "Example copy",
    }
    result = analyze_copy(row)
    assert result["has_hook"] is True
    assert result["has_cta"] is True


def test_completeness_is_not_roas():
    result = creative_completeness({"hook": "x", "cta": "y"})
    assert result["score"] == 2.5
    assert "not a prediction of ROAS" in result["interpretation"]


def test_fatigue_signal():
    result = fatigue_signal([
        {"ctr": 2.5, "frequency": 1.5, "cpa": 8},
        {"ctr": 1.7, "frequency": 2.3, "cpa": 11},
    ])
    assert result["signal"] is True


def test_rank_creatives_flags_small_samples():
    result = rank_creatives([
        {"ad_id": "a", "spend": 20, "conversions": 2, "roas": 4},
        {"ad_id": "b", "spend": 200, "conversions": 20, "roas": 3},
    ])
    assert result[0]["ad_id"] == "a"
    assert result[0]["sample_warning"] is True
