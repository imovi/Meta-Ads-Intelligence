import json
from pathlib import Path

from scripts.browser_vision import (
    BrowserObservation,
    browser_analysis_contract,
    creative_checklist,
    extract_visible_metric_rows,
    observation_from_dict,
    validate_observation,
)


def load_sample():
    return json.loads(Path("examples/browser_observation.json").read_text())


def test_observation_validation_and_extraction():
    observation = observation_from_dict(load_sample())
    assert isinstance(observation, BrowserObservation)
    assert validate_observation(observation) == []
    rows = extract_visible_metric_rows([observation])
    assert rows[0]["spend"] == 120
    assert rows[0]["evidence"] == "browser_observed"


def test_creative_checklist_is_observation_only():
    result = creative_checklist(load_sample()["creative"])
    assert result["observed_components"] == 7
    assert "performance prediction" in result["note"]


def test_browser_contract_forbids_secret_requests_and_writes():
    contract = browser_analysis_contract()
    assert "request passwords/cookies/tokens in chat" in contract["must_not"]
    assert "execute account changes during analysis" in contract["must_not"]
