import json
from pathlib import Path

from scripts.budget_allocator import classify_campaign, simulate_allocation


def load_sample():
    return json.loads(Path("examples/budget_scenario.json").read_text())


def test_classifies_scale_reduce_and_test():
    sample = load_sample()
    assert classify_campaign(sample["campaigns"][0], target_roas=2.5) == "scale"
    assert classify_campaign(sample["campaigns"][2], target_roas=2.5) == "hold"
    assert classify_campaign(sample["campaigns"][3], target_roas=2.5) == "test"


def test_simulation_preserves_total_budget():
    sample = load_sample()
    result = simulate_allocation(sample["campaigns"], sample["total_budget"], target_roas=sample["target_roas"])
    assert result["total_budget"] == 1000
    assert result["test_pool"] == 100
    assert result["action_allowed"] is False
    assert all(item["proposed_daily_budget"] >= 0 for item in result["allocations"])
