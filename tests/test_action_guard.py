from scripts.action_guard import ProposedChange, confirmation_text, validate_proposal


def test_high_impact_change_is_marked():
    proposal = ProposedChange(
        account="act_123",
        target_type="campaign",
        target_id="cmp_1",
        target_name="Sales",
        operation="budget_increase",
        current={"daily_budget": 50},
        requested={"daily_budget": 100},
        reason="Strong efficiency with sufficient conversion volume.",
    )
    assert proposal.high_impact is True
    assert validate_proposal(proposal) == []
    text = confirmation_text(proposal)
    assert "Current" in text and "New" in text


def test_incomplete_proposal_is_rejected():
    proposal = ProposedChange(
        account="",
        target_type="campaign",
        target_id="",
        target_name="",
        operation="pause",
        current={},
        requested={},
    )
    errors = validate_proposal(proposal)
    assert "Missing account scope." in errors
    assert "Missing target object ID." in errors
    assert "Missing requested state." in errors
