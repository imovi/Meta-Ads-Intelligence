import json
from pathlib import Path

from scripts.scaling_intelligence import assess_account, assess_scaling


def load_rows():
    return json.loads(Path("examples/scaling_scenarios.json").read_text())


def test_winner_is_scale_candidate():
    result = assess_scaling(load_rows()[0], target_roas=2.5, target_cpa=20)
    assert result["recommendation"] == "scale"
    assert result["action_allowed"] is False


def test_fatigue_blocks_scale():
    result = assess_scaling(load_rows()[2], target_roas=2.5, target_cpa=20)
    assert result["recommendation"] != "scale"
    assert "creative fatigue signal" in result["evidence"]


def test_low_volume_becomes_test():
    result = assess_scaling(load_rows()[3], target_roas=2.5, target_cpa=20)
    assert result["recommendation"] == "test"


def test_account_ordering():
    result = assess_account(load_rows(), target_roas=2.5, target_cpa=20)
    assert result[0]["recommendation"] == "scale"
