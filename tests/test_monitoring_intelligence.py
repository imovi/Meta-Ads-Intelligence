from scripts.monitoring_intelligence import detect_alerts, monitor_account


def test_detects_material_changes():
    current = {"roas": 2.4, "cpa": 24, "ctr": 1.8, "spend": 420, "conversions": 17}
    previous = {"roas": 3.3, "cpa": 17, "ctr": 2.4, "spend": 300, "conversions": 25}
    alerts = detect_alerts(current, previous)
    metrics = {a["metric"] for a in alerts}
    assert "roas" in metrics
    assert "cpa" in metrics
    assert "conversions" in metrics


def test_fatigue_is_high_priority_and_read_only():
    result = monitor_account(
        [{"id":"a","name":"Test","roas":3,"cpa":10,"fatigue_signal":True}],
        [{"id":"a","name":"Test","roas":3,"cpa":10}],
    )
    assert result["status"] == "alerts_detected"
    assert result["action_allowed"] is False
    assert any(a["metric"] == "creative_fatigue" for a in result["items"][0]["alerts"])
