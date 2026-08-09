from scripts.autonomous_research import build_research_plan, record_observation, summarize_research


def test_research_plan_is_browser_first_and_read_only():
    plan = build_research_plan("Skincare", competitors=["Brand A"], market="Malaysia")
    assert plan["browser_preferred"] is True
    assert plan["api_required"] is False
    assert plan["private_data_allowed"] is False
    assert "collect_public_ad_observations" in plan["steps"]


def test_observation_evidence_types():
    observations = record_observation([], source="Meta Ad Library", subject="Brand A", finding="UGC observed")
    observations = record_observation(observations, source="analysis", subject="market", finding="possible gap", evidence_type="inferred")
    summary = summarize_research(build_research_plan("Skincare"), observations)
    assert summary["evidence_counts"]["observed"] == 1
    assert summary["evidence_counts"]["inferred"] == 1
