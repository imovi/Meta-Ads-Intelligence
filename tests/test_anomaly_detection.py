from scripts.anomaly_detection import detect_period_anomalies, detect_tracking_anomaly


def test_detects_material_cpa_increase():
    findings = detect_period_anomalies(
        {"cpa": 14, "roas": 2.5, "ctr": 1.8, "cpm": 5.5, "frequency": 2.4, "conversions": 16},
        {"cpa": 10, "roas": 3.8, "ctr": 2.5, "cpm": 5, "frequency": 1.8, "conversions": 20},
    )
    metrics = {item["metric"] for item in findings}
    assert "cpa" in metrics
    assert "roas" in metrics


def test_tracking_validation():
    issues = detect_tracking_anomaly({"spend": 100, "clicks": 120, "impressions": 100, "conversions": 3, "revenue": 100})
    assert any("clicks exceed impressions" in issue.lower() for issue in issues)
