"""Read-only monitoring and alert prioritization for Meta Ads metrics."""

from __future__ import annotations

from typing import Any, Iterable


def _num(row: dict[str, Any], key: str) -> float | None:
    try:
        value = row.get(key)
        return None if value is None else float(value)
    except (TypeError, ValueError):
        return None


def pct_change(current: float | None, previous: float | None) -> float | None:
    if current is None or previous in (None, 0):
        return None
    return (current - previous) / previous * 100


def detect_alerts(current: dict[str, Any], previous: dict[str, Any] | None = None, *, ctr_drop_pct: float = 20, cpa_rise_pct: float = 25, roas_drop_pct: float = 20, spend_rise_pct: float = 30, conversion_drop_pct: float = 25) -> list[dict[str, Any]]:
    alerts: list[dict[str, Any]] = []
    previous = previous or {}
    rules = [
        ("ctr", "CTR drop", "high", "lower", ctr_drop_pct),
        ("cpa", "CPA increase", "high", "higher", cpa_rise_pct),
        ("roas", "ROAS drop", "critical", "lower", roas_drop_pct),
        ("spend", "Spend spike", "medium", "higher", spend_rise_pct),
        ("conversions", "Conversion drop", "critical", "lower", conversion_drop_pct),
    ]
    for metric, title, severity, direction, threshold in rules:
        change = pct_change(_num(current, metric), _num(previous, metric))
        if change is None:
            continue
        triggered = change <= -threshold if direction == "lower" else change >= threshold
        if triggered:
            alerts.append({
                "metric": metric,
                "title": title,
                "severity": severity,
                "change_pct": round(change, 2),
                "current": _num(current, metric),
                "previous": _num(previous, metric),
                "recommended_check": "Review delivery, attribution, audience, placement, creative fatigue, and tracking before taking action.",
            })
    return sorted(alerts, key=lambda x: {"critical": 0, "high": 1, "medium": 2, "low": 3}.get(x["severity"], 9))


def monitor_account(current_rows: Iterable[dict[str, Any]], previous_rows: Iterable[dict[str, Any]] | None = None) -> dict[str, Any]:
    current = list(current_rows)
    previous = list(previous_rows or [])
    current_by_id = {str(r.get("id") or r.get("campaign_id") or r.get("campaign_name")): r for r in current}
    previous_by_id = {str(r.get("id") or r.get("campaign_id") or r.get("campaign_name")): r for r in previous}
    findings = []
    for key, row in current_by_id.items():
        alerts = detect_alerts(row, previous_by_id.get(key))
        if row.get("fatigue_signal"):
            alerts.append({"metric": "creative_fatigue", "title": "Creative fatigue signal", "severity": "high", "change_pct": None, "recommended_check": "Review frequency, CTR trend, CPA trend, and fresh creative tests."})
        findings.append({"id": key, "name": row.get("name") or row.get("campaign_name"), "alerts": alerts})
    all_alerts = [a for item in findings for a in item["alerts"]]
    return {
        "status": "alerts_detected" if all_alerts else "no_material_alerts",
        "items": findings,
        "alert_count": len(all_alerts),
        "highest_severity": next((x["severity"] for x in all_alerts), None),
        "action_allowed": False,
        "note": "Monitoring produces diagnostic alerts only. It does not pause, edit, or budget-change campaigns.",
    }
