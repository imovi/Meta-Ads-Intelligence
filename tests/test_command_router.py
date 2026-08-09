from scripts.command_router import explain_route, route


def test_analysis_is_default():
    result = route("Why is my CPA high?")
    assert result.mode == "analyze"
    assert result.action_requested is False


def test_competitor_route():
    assert route("Analyze my competitor's Facebook ads").mode == "competitor"


def test_audit_route():
    assert route("Audit my whole Meta ad account").mode == "audit"


def test_action_requires_confirmation():
    result = route("Increase campaign budget to $100 per day")
    assert result.mode == "action"
    assert result.action_requested is True
    assert result.confirmation_required is True


def test_unclear_change_does_not_invent_operation():
    result = explain_route("Can you change campaign ABC?")
    assert result["mode"] == "action"
    assert result["confirmation_required"] is True
