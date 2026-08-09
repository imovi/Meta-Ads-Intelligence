from scripts.strategy_engine import classify_health, next_7_day_plan, rank_for_budget_allocation, recommend


def test_healthy_requires_reasonable_evidence():
    assert classify_health({"spend": 200, "conversions": 10, "roas": 4}, target_roas=3) == "healthy"


def test_no_conversion_is_critical():
    assert classify_health({"spend": 100, "conversions": 0, "roas": 0}, target_roas=2) == "critical"


def test_recommendation_checks_frequency():
    result = recommend({"spend": 200, "conversions": 12, "roas": 3.5, "ctr": 1.8, "frequency": 3.4}, target_roas=3)
    assert result["health"] == "healthy"
    assert any("fatigue" in action.lower() for action in result["actions"])


def test_budget_rank_flags_small_sample():
    result = rank_for_budget_allocation([
        {"id": "a", "spend": 20, "conversions": 2, "roas": 8},
        {"id": "b", "spend": 200, "conversions": 20, "roas": 4},
    ])
    assert result[0]["id"] == "b"
    assert result[1]["evidence_weak"] is True


def test_next_7_day_plan_prioritizes_critical():
    plan = next_7_day_plan([
        {"id": "healthy", "name": "Healthy", "spend": 200, "conversions": 10, "roas": 4},
        {"id": "broken", "name": "Broken", "spend": 100, "conversions": 0, "roas": 0},
    ], target_roas=2)
    assert plan[0]["id"] == "broken"
    assert plan[0]["priority"] == "High"
