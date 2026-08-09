import json
from pathlib import Path

from scripts.creative_test_generator import build_ab_matrix, generate_creative_tests


def load_sample():
    return json.loads(Path("examples/creative_test_matrix.json").read_text())


def test_generates_controlled_tests():
    sample = load_sample()
    result = generate_creative_tests(sample["winner"], fatigue=sample["fatigue"], count=5)
    assert len(result) == 5
    assert result[0]["change"] == "hook"
    assert "success_metric" in result[0]
    assert "stop_condition" in result[0]


def test_matrix_keeps_control_separate():
    sample = load_sample()
    result = build_ab_matrix(sample["winner"], fatigue=sample["fatigue"])
    assert result["control"]["id"] == "ad_001"
    assert result["method"] == "one_primary_variable_at_a_time"
    assert "guarantee" in result["warning"]
