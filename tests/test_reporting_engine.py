from scripts.reporting_engine import aggregate, build_markdown_report, compare_periods


def test_aggregate_uses_totals():
    result = aggregate([
        {"spend": 100, "impressions": 10000, "clicks": 200, "conversions": 10, "revenue": 500},
        {"spend": 50, "impressions": 5000, "clicks": 50, "conversions": 5, "revenue": 200},
    ])
    assert result["spend"] == 150
    assert result["impressions"] == 15000
    assert round(result["ctr"], 4) == round(250 / 15000 * 100, 4)
    assert result["cpa"] == 10
    assert round(result["roas"], 4) == round(700 / 150, 4)


def test_period_comparison():
    result = compare_periods({"spend": 120, "roas": 3}, {"spend": 100, "roas": 2})
    assert result["spend"]["absolute_change"] == 20
    assert result["spend"]["percent_change"] == 20
    assert result["roas"]["percent_change"] == 50


def test_markdown_report_contains_decision_sections():
    report = build_markdown_report(
        title="Weekly Meta Ads Report",
        start_date="2026-08-01",
        end_date="2026-08-07",
        rows=[{"id": "a", "name": "Campaign A", "spend": 100, "impressions": 10000, "clicks": 300, "conversions": 10, "revenue": 400, "roas": 4}],
        summary="Performance was stable.",
        recommendations=["Test a new creative hook."],
    )
    assert "Executive Summary" in report
    assert "KPI Snapshot" in report
    assert "Top Performers" in report
    assert "Recommended Actions" in report
    assert "Test a new creative hook." in report
