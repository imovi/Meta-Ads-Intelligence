from scripts.client_report import build_client_report, kpi_snapshot


def test_kpi_snapshot_uses_aggregate_totals():
    rows = [
        {"spend": 500, "impressions": 70000, "clicks": 2100, "conversions": 40, "revenue": 2000},
        {"spend": 250, "impressions": 30000, "clicks": 1200, "conversions": 25, "revenue": 1000},
    ]
    kpis = kpi_snapshot(rows)
    # Aggregate totals: spend 750, conversions 65, revenue 3000.
    assert kpis["roas"] == 4.0
    assert round(kpis["cpa"], 2) == 11.54
    assert round(kpis["ctr"], 2) == 3.3


def test_report_contains_client_sections():
    report = build_client_report(
        title="Weekly Report",
        period="Aug 3–9",
        rows=[{"spend": 100, "impressions": 1000, "clicks": 30, "conversions": 5, "revenue": 300}],
        executive_summary="Performance improved.",
        wins=["ROAS improved"],
        problems=["One creative is fatigued"],
        recommendations=["Launch a new hook"],
        next_7_days=["Review after sufficient data"],
        source="Ads Manager export",
    )
    assert "Executive Summary" in report
    assert "KPI Snapshot" in report
    assert "What Worked" in report
    assert "Next 7 Days" in report
    assert "Ads Manager export" in report
