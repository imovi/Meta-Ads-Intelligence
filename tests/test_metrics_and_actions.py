from scripts.normalize_metrics import derive_metrics
from scripts.action_guard import ProposedChange, confirmation_text, validate_proposal
from scripts.mock_meta_api import find, set_daily_budget, set_status


def test_metric_derivation():
    row = derive_metrics({
        "spend": 100,
        "impressions": 20000,
        "clicks": 400,
        "reach": 10000,
        "conversions": 10,
        "revenue": 500,
    })
    assert row["cpm"] == 5
    assert row["ctr"] == 2
    assert row["cpc"] == 0.25
    assert row["cpa"] == 10
    assert row["conversion_rate"] == 2.5
    assert row["roas"] == 5
    assert row["frequency"] == 2


def test_action_proposal_requires_target_and_account():
    proposal = ProposedChange(
        account="act_mock_001",
        target_type="campaign",
        target_id="camp_001",
        target_name="Prospecting - Sales",
        operation="budget_increase",
        current={"daily_budget": 100},
        requested={"daily_budget": 125},
        reason="Stable efficiency.",
    )
    assert validate_proposal(proposal) == []
    assert proposal.high_impact is True
    assert "Current:" in confirmation_text(proposal)
    assert "New:" in confirmation_text(proposal)


def test_mock_action_changes_state():
    before = find("camp_001")
    assert before["daily_budget"] == 100
    after = set_daily_budget("camp_001", 125)
    assert after["daily_budget"] == 125

    ad = find("ad_001")
    assert ad["status"] == "ACTIVE"
    paused = set_status("ad_001", "PAUSED")
    assert paused["status"] == "PAUSED"
