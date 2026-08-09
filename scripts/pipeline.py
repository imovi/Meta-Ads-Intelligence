"""End-to-end orchestration for Meta Ads Intelligence.

This layer connects routing, data normalization, diagnostics, strategy,
creative signals, anomaly detection, auditing, and reporting. It intentionally
keeps account writes outside the analysis pipeline.
"""

from __future__ import annotations

from typing import Any, Iterable

from account_audit import audit_account, audit_score
from anomaly_detection import scan as scan_anomalies
from command_router import route
from creative_intelligence import rank_creatives
from reporting_engine import aggregate, build_markdown_report
from strategy_engine import next_7_day_plan


def _derive_basic_metrics(row: dict[str, Any]) -> dict[str, Any]:
    item = dict(row)
    spend = float(item.get("spend") or 0)
    impressions = float(item.get("impressions") or 0)
    clicks = float(item.get("clicks") or 0)
    conversions = float(item.get("conversions") or 0)
    revenue = float(item.get("revenue") or 0)
    reach = float(item.get("reach") or 0)
    item.setdefault("cpm", spend / impressions * 1000 if impressions else 0)
    item.setdefault("ctr", clicks / impressions * 100 if impressions else 0)
    item.setdefault("cpc", spend / clicks if clicks else 0)
    item.setdefault("cpa", spend / conversions if conversions else 0)
    item.setdefault("roas", revenue / spend if spend else 0)
    item.setdefault("frequency", impressions / reach if reach else 0)
    return item


def run_analysis(rows: Iterable[dict[str, Any]], *, previous_rows: Iterable[dict[str, Any]] | None = None, target_cpa: float | None = None, target_roas: float | None = None) -> dict[str, Any]:
    current = [_derive_basic_metrics(row) for row in rows]
    previous = [_derive_basic_metrics(row) for row in previous_rows] if previous_rows is not None else None

    audit = audit_account(current, target_cpa=target_cpa, target_roas=target_roas)
    score = audit_score(audit)
    strategy = next_7_day_plan(current, target_cpa=target_cpa, target_roas=target_roas)
    creative = rank_creatives(current)
    anomalies = []
    if previous:
        # Compare aggregate periods rather than pretending row IDs line up.
        current_total = aggregate(current)
        previous_total = aggregate(previous)
        anomalies = scan_anomalies([previous_total, current_total])

    return {
        "summary": aggregate(current),
        "audit": audit,
        "audit_score": score,
        "strategy": strategy,
        "creative_ranking": creative,
        "anomalies": anomalies,
        "action_allowed": False,
        "note": "This pipeline is analysis-only. Explicit account actions must use the Action Guard and Meta API write layer.",
    }


def dispatch(user_text: str, rows: Iterable[dict[str, Any]], **kwargs: Any) -> dict[str, Any]:
    """Route a request and run only the analysis pipeline here.

    Action mode is surfaced but deliberately not executed by this function.
    """
    decision = route(user_text)
    if decision.mode == "action":
        return {
            "route": decision.__dict__,
            "status": "action_required",
            "message": "An account-changing operation was requested. Resolve target/current state and pass the proposed change through Action Guard before any write.",
        }

    result = run_analysis(rows, **kwargs)
    result["route"] = decision.__dict__
    return result


def build_report_from_analysis(analysis: dict[str, Any], *, title: str, start_date: str, end_date: str) -> str:
    recommendations = []
    for item in analysis.get("strategy", [])[:7]:
        recommendations.extend(item.get("next_actions", []))
    summary = (
        f"Directional account health: {analysis['audit_score']['label']} "
        f"({analysis['audit_score']['score']}/100). "
        f"{analysis['audit']['high_priority_count']} high-priority finding(s) were identified."
    )
    return build_markdown_report(
        title=title,
        start_date=start_date,
        end_date=end_date,
        rows=analysis.get("audit", {}).get("objects", []),
        summary=summary,
        recommendations=dict.fromkeys(recommendations),
    )
