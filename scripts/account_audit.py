"""Account-level Meta Ads audit orchestration.

Combines supplied campaign/ad-set/ad rows, KPI calculations, strategy signals,
anomalies, and creative signals into a prioritized audit. It never executes
account changes.
"""

from __future__ import annotations

from typing import Any, Iterable

from anomaly_detection import detect_tracking_anomaly
from creative_intelligence import creative_completeness
from strategy_engine import classify_health, recommend


def _num(row: dict[str, Any], key: str) -> float:
    try:
        return float(row.get(key) or 0)
    except (TypeError, ValueError):
        return 0.0


def audit_object(row: dict[str, Any], *, target_cpa: float | None = None, target_roas: float | None = None) -> dict[str, Any]:
    health = classify_health(row, target_cpa=target_cpa, target_roas=target_roas)
    strategy = recommend(row, target_cpa=target_cpa, target_roas=target_roas)
    tracking = detect_tracking_anomaly(row)
    creative = creative_completeness(row)

    findings: list[str] = []
    if tracking:
        findings.extend(tracking)
    findings.extend(strategy["actions"])

    return {
        "id": row.get("id") or row.get("ad_id") or row.get("adset_id") or row.get("campaign_id"),
        "name": row.get("name") or row.get("ad_name") or row.get("adset_name") or row.get("campaign_name") or "Unknown",
        "health": health,
        "priority": strategy["priority"],
        "spend": _num(row, "spend"),
        "conversions": _num(row, "conversions"),
        "cpa": _num(row, "cpa"),
        "roas": _num(row, "roas"),
        "creative_completeness": creative["score"],
        "tracking_warnings": tracking,
        "findings": findings,
    }


def audit_account(rows: Iterable[dict[str, Any]], *, target_cpa: float | None = None, target_roas: float | None = None) -> dict[str, Any]:
    audits = [audit_object(row, target_cpa=target_cpa, target_roas=target_roas) for row in rows]
    priority_order = {"High": 0, "Medium": 1, "Low": 2}
    audits.sort(key=lambda item: (priority_order.get(item["priority"], 3), -item["spend"]))

    counts: dict[str, int] = {}
    for item in audits:
        counts[item["health"]] = counts.get(item["health"], 0) + 1

    high_priority = [item for item in audits if item["priority"] == "High"]
    return {
        "objects_audited": len(audits),
        "health_counts": counts,
        "high_priority_count": len(high_priority),
        "top_findings": high_priority[:10],
        "objects": audits,
        "note": "Audit findings are decision-support signals. They do not authorize or execute account changes.",
    }


def audit_score(audit: dict[str, Any]) -> dict[str, Any]:
    """Produce a simple account-health score from audit state counts.

    This score is directional and should be used alongside the detailed findings.
    """
    total = max(int(audit.get("objects_audited", 0)), 1)
    counts = audit.get("health_counts", {})
    critical = counts.get("critical", 0)
    needs = counts.get("needs_attention", 0)
    healthy = counts.get("healthy", 0)
    score = 50 + (healthy / total) * 50 - (needs / total) * 25 - (critical / total) * 50
    score = max(0, min(100, round(score)))
    return {
        "score": score,
        "label": "healthy" if score >= 75 else "needs_attention" if score >= 45 else "critical",
        "note": "Directional audit score; not a Meta-provided account quality metric.",
    }
