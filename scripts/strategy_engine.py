"""Strategy and optimization decision engine.

Produces recommendations from supplied Meta Ads metrics. It does not execute
account changes. Any action must pass through the explicit action workflow.
"""

from __future__ import annotations

from typing import Any, Iterable


def _num(row: dict[str, Any], key: str, default: float = 0.0) -> float:
    try:
        return float(row.get(key, default) or default)
    except (TypeError, ValueError):
        return default


def classify_health(row: dict[str, Any], *, target_cpa: float | None = None, target_roas: float | None = None) -> str:
    spend = _num(row, "spend")
    conversions = _num(row, "conversions")
    cpa = _num(row, "cpa") if row.get("cpa") is not None else (spend / conversions if conversions else 0)
    roas = _num(row, "roas")

    if spend <= 0:
        return "insufficient_data"
    if target_roas is not None and roas >= target_roas and conversions >= 5:
        return "healthy"
    if target_cpa is not None and cpa <= target_cpa and conversions >= 5:
        return "healthy"
    if conversions == 0:
        return "critical"
    if (target_roas is not None and roas < target_roas) or (target_cpa is not None and cpa > target_cpa):
        return "needs_attention"
    return "watch"


def recommend(row: dict[str, Any], *, target_cpa: float | None = None, target_roas: float | None = None) -> dict[str, Any]:
    health = classify_health(row, target_cpa=target_cpa, target_roas=target_roas)
    spend = _num(row, "spend")
    conversions = _num(row, "conversions")
    cpa = _num(row, "cpa") if row.get("cpa") is not None else (spend / conversions if conversions else 0)
    roas = _num(row, "roas")
    ctr = _num(row, "ctr")
    frequency = _num(row, "frequency")

    actions: list[str] = []
    priority = "Low"

    if health == "critical":
        priority = "High"
        actions.append("Investigate conversion tracking, offer/landing page, audience fit, and creative before adding budget.")
    elif health == "healthy":
        priority = "Medium"
        if conversions >= 10:
            actions.append("Consider gradual scaling after checking stability, frequency, audience size, and creative fatigue.")
        else:
            actions.append("Keep collecting data before making an aggressive scaling decision.")
    elif health == "needs_attention":
        priority = "High"
        actions.append("Diagnose the weakest funnel stage before changing budget materially.")
    else:
        actions.append("Continue monitoring and compare against the previous period or account baseline.")

    if ctr and ctr < 1:
        actions.append("Test new hooks/creative angles because CTR is relatively weak; validate against account and placement benchmarks.")
    if frequency >= 3:
        actions.append("Check creative fatigue and audience saturation before scaling spend.")

    return {
        "health": health,
        "priority": priority,
        "cpa": cpa,
        "roas": roas,
        "actions": actions,
        "note": "Recommendations are evidence-based hypotheses; confirm tracking, attribution, sample size, and business context before acting.",
    }


def rank_for_budget_allocation(rows: Iterable[dict[str, Any]], *, min_spend: float = 50, min_conversions: float = 5) -> list[dict[str, Any]]:
    """Rank candidates while explicitly flagging weak evidence."""
    result = []
    for row in rows:
        item = dict(row)
        spend = _num(item, "spend")
        conversions = _num(item, "conversions")
        roas = _num(item, "roas")
        evidence_weak = spend < min_spend or conversions < min_conversions
        item["evidence_weak"] = evidence_weak
        item["allocation_score"] = roas if not evidence_weak else roas * 0.5
        item["recommendation"] = "scale_candidate" if not evidence_weak and roas > 1 else "collect_more_data_or_fix"
        result.append(item)
    # On equal scores prefer the better-evidenced candidate, so a small-sample
    # row cannot outrank a proven one purely through sort stability.
    return sorted(result, key=lambda x: (x["allocation_score"], not x["evidence_weak"]), reverse=True)


def next_7_day_plan(rows: Iterable[dict[str, Any]], *, target_cpa: float | None = None, target_roas: float | None = None) -> list[dict[str, Any]]:
    plan = []
    for row in rows:
        recommendation = recommend(row, target_cpa=target_cpa, target_roas=target_roas)
        plan.append({
            "id": row.get("id") or row.get("ad_id") or row.get("campaign_id"),
            "name": row.get("name") or row.get("ad_name") or row.get("campaign_name"),
            "priority": recommendation["priority"],
            "health": recommendation["health"],
            "next_actions": recommendation["actions"],
        })
    order = {"High": 0, "Medium": 1, "Low": 2}
    return sorted(plan, key=lambda x: order.get(x["priority"], 3))
