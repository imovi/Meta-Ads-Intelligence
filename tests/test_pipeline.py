import json
from pathlib import Path

from scripts.pipeline import build_report_from_analysis, dispatch, run_analysis


def load_rows():
    return json.loads(Path("examples/pipeline_rows.json").read_text())


def test_pipeline_combines_modules():
    result = run_analysis(load_rows(), target_roas=2)
    assert "summary" in result
    assert "audit" in result
    assert "strategy" in result
    assert "creative_ranking" in result
    assert result["action_allowed"] is False


def test_dispatch_keeps_action_out_of_analysis_pipeline():
    result = dispatch("Pause campaign ABC", load_rows())
    assert result["status"] == "action_required"
    assert "Action Guard" in result["message"]


def test_dispatch_analyzes_normal_request():
    result = dispatch("Analyze these ads", load_rows())
    assert result["route"]["mode"] == "analyze"
    assert "summary" in result


def test_build_report():
    analysis = run_analysis(load_rows(), target_roas=2)
    report = build_report_from_analysis(analysis, title="Meta Ads Report", start_date="2026-08-01", end_date="2026-08-10")
    assert "# Meta Ads Report" in report
    assert "KPI Snapshot" in report
