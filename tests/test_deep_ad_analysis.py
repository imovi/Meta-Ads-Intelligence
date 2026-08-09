from scripts.deep_ad_analysis import analyze_ad


def test_deep_analysis_keeps_observation_boundaries():
    result = analyze_ad({
        "id": "ad_1",
        "source": "browser_observed",
        "hook": "Problem hook",
        "copy": "Benefit copy",
        "offer": "20% off",
        "proof": "Testimonial",
        "cta": "Shop now",
        "format": "video",
        "hook_score": 8,
        "offer_score": 7,
        "proof_score": 9,
        "cta_score": 8,
        "visual_score": 8,
        "ctr": 2.4,
        "cpc": 0.32,
        "cpa": 12.5,
        "roas": 3.8,
    })
    assert result["source"] == "browser_observed"
    assert result["confidence"] == "high"
    assert result["dimensions"]["hook"] == "strong"


def test_missing_creative_fields_reduce_confidence():
    result = analyze_ad({"id": "ad_2", "ctr": 1.2})
    assert result["confidence"] == "limited_by_missing_creative_observations"
    assert "hook" in result["missing_observations"]
