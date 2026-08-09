import json
from pathlib import Path

from scripts.account_audit import audit_account, audit_score


def load_rows():
    return json.loads(Path("examples/account_audit_rows.json").read_text())


def test_account_audit_prioritizes_critical_objects():
    result = audit_account(load_rows(), target_roas=2)
    assert result["objects_audited"] == 2
    assert result["health_counts"]["critical"] == 1
    assert result["top_findings"][0]["id"] == "campaign_critical"


def test_audit_score_is_directional():
    audit = audit_account(load_rows(), target_roas=2)
    score = audit_score(audit)
    assert 0 <= score["score"] <= 100
    assert "Meta-provided" in score["note"]
