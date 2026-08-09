"""Generate concise client-facing reports from normalized Meta Ads analysis data."""

from __future__ import annotations

from typing import Any, Iterable


def _num(row: dict[str, Any], key: str) -> float:
    try:
        return float(row.get(key) or 0)
    except (TypeError, ValueError):
        return 0.0


def kpi_snapshot(rows: Iterable[dict[str, Any]]) -> dict[str, float]:
    rows = list(rows)
    spend = sum(_num(r, "spend") for r in rows)
    conversions = sum(_num(r, "conversions") for r in rows)
    revenue = sum(_num(r, "revenue") for r in rows)
    impressions = sum(_num(r, "impressions") for r in rows)
    clicks = sum(_num(r, "clicks") for r in rows)
    return {
        "spend": spend,
        "conversions": conversions,
        "revenue": revenue,
        "roas": revenue / spend if spend else 0,
        "cpa": spend / conversions if conversions else 0,
        "ctr": clicks / impressions * 100 if impressions else 0,
        "impressions": impressions,
        "clicks": clicks,
    }


def build_client_report(*, title: str, period: str, rows: Iterable[dict[str, Any]], executive_summary: str, wins: list[str] | None = None, problems: list[str] | None = None, recommendations: list[str] | None = None, next_7_days: list[str] | None = None, source: str = "unknown") -> str:
    kpis = kpi_snapshot(rows)
    wins = wins or []
    problems = problems or []
    recommendations = recommendations or []
    next_7_days = next_7_days or []

    def bullets(items: list[str]) -> str:
        return "\n".join(f"- {item}" for item in items) if items else "- None identified from the supplied evidence."

    return f"""# {title}\n\n**Period:** {period}  \n**Data source:** {source}\n\n## Executive Summary\n\n{executive_summary}\n\n## KPI Snapshot\n\n| KPI | Value |\n|---|---:|\n| Spend | {kpis['spend']:.2f} |\n| Revenue | {kpis['revenue']:.2f} |\n| ROAS | {kpis['roas']:.2f}x |\n| Conversions | {kpis['conversions']:.0f} |\n| CPA | {kpis['cpa']:.2f} |\n| CTR | {kpis['ctr']:.2f}% |\n| Impressions | {kpis['impressions']:.0f} |\n| Clicks | {kpis['clicks']:.0f} |\n\n## What Worked\n\n{bullets(wins)}\n\n## What Needs Attention\n\n{bullets(problems)}\n\n## Recommended Actions\n\n{bullets(recommendations)}\n\n## Next 7 Days\n\n{bullets(next_7_days)}\n\n## Evidence & Limitations\n\nRecommendations are based only on the supplied data and observations. Missing attribution, tracking, audience, placement, or business-context data can limit conclusions. No account changes are implied by this report.\n"""
