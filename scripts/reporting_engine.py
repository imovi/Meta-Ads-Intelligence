"""Client-ready reporting utilities for Meta Ads Intelligence."""

from __future__ import annotations

from datetime import date
from typing import Any, Iterable


def _num(row: dict[str, Any], key: str) -> float:
    try:
        return float(row.get(key) or 0)
    except (TypeError, ValueError):
        return 0.0


def aggregate(rows: Iterable[dict[str, Any]]) -> dict[str, float]:
    rows = list(rows)
    spend = sum(_num(r, "spend") for r in rows)
    impressions = sum(_num(r, "impressions") for r in rows)
    reach = sum(_num(r, "reach") for r in rows)
    clicks = sum(_num(r, "clicks") for r in rows)
    conversions = sum(_num(r, "conversions") for r in rows)
    revenue = sum(_num(r, "revenue") for r in rows)
    return {
        "spend": spend,
        "impressions": impressions,
        "reach": reach,
        "clicks": clicks,
        "conversions": conversions,
        "revenue": revenue,
        "cpm": spend / impressions * 1000 if impressions else 0,
        "ctr": clicks / impressions * 100 if impressions else 0,
        "cpc": spend / clicks if clicks else 0,
        "cpa": spend / conversions if conversions else 0,
        "roas": revenue / spend if spend else 0,
    }


def compare_periods(current: dict[str, Any], previous: dict[str, Any]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key in ("spend", "impressions", "reach", "clicks", "conversions", "revenue", "cpm", "ctr", "cpc", "cpa", "roas"):
        now = _num(current, key)
        old = _num(previous, key)
        result[key] = {
            "current": now,
            "previous": old,
            "absolute_change": now - old,
            "percent_change": ((now - old) / old * 100) if old else None,
        }
    return result


def rank_rows(rows: Iterable[dict[str, Any]], metric: str = "roas", reverse: bool = True) -> list[dict[str, Any]]:
    items = []
    for row in rows:
        item = dict(row)
        item["_rank_value"] = _num(item, metric)
        items.append(item)
    return sorted(items, key=lambda x: x["_rank_value"], reverse=reverse)


def _fmt(value: float, digits: int = 2) -> str:
    return f"{value:,.{digits}f}"


def build_markdown_report(
    *,
    title: str,
    start_date: str,
    end_date: str,
    rows: Iterable[dict[str, Any]],
    previous: dict[str, Any] | None = None,
    summary: str = "",
    recommendations: Iterable[str] = (),
) -> str:
    rows = list(rows)
    totals = aggregate(rows)
    lines = [
        f"# {title}",
        "",
        f"**Period:** {start_date} → {end_date}",
        "",
        "## Executive Summary",
        "",
        summary or "Performance summary generated from the supplied dataset.",
        "",
        "## KPI Snapshot",
        "",
        "| KPI | Value |",
        "|---|---:|",
        f"| Spend | {_fmt(totals['spend'])} |",
        f"| Revenue | {_fmt(totals['revenue'])} |",
        f"| ROAS | {_fmt(totals['roas'])}x |",
        f"| Conversions | {_fmt(totals['conversions'], 0)} |",
        f"| CPA | {_fmt(totals['cpa'])} |",
        f"| CTR | {_fmt(totals['ctr'])}% |",
        f"| CPC | {_fmt(totals['cpc'])} |",
        f"| CPM | {_fmt(totals['cpm'])} |",
        "",
    ]

    if previous:
        comparison = compare_periods(totals, previous)
        lines += ["## Period Comparison", "", "| KPI | Change |", "|---|---:|"]
        for key in ("spend", "revenue", "conversions", "cpa", "roas", "ctr"):
            pct = comparison[key]["percent_change"]
            text = "n/a" if pct is None else f"{pct:+.1f}%"
            lines.append(f"| {key.upper()} | {text} |")
        lines.append("")

    ranked = rank_rows(rows, "roas")
    lines += ["## Top Performers", "", "| Name | ROAS | Spend | Conversions |", "|---|---:|---:|---:|"]
    for row in ranked[:5]:
        name = row.get("name") or row.get("ad_name") or row.get("campaign_name") or row.get("id") or "Unknown"
        lines.append(f"| {name} | {_fmt(_num(row, 'roas'))}x | {_fmt(_num(row, 'spend'))} | {_fmt(_num(row, 'conversions'), 0)} |")
    lines.append("")

    lines += ["## Recommended Actions", ""]
    recommendations = list(recommendations)
    if recommendations:
        lines.extend(f"- {item}" for item in recommendations)
    else:
        lines.append("- No recommendations were supplied; run the Strategy Engine for prioritized actions.")
    lines += ["", "## Data Notes", "", "- Metrics are calculated from the supplied dataset.", "- Public competitor observations do not establish private spend, CPA, ROAS, or targeting.", "- Validate attribution, sample size, and tracking before making account changes.", ""]
    return "\n".join(lines)


def report_filename(prefix: str = "meta-ads-report") -> str:
    return f"{prefix}-{date.today().isoformat()}.md"
