"""Detect repeatable winning creative patterns from supplied ad data.

A winner is only considered meaningful when outcome volume is sufficient. The
engine separates observed performance from hypotheses about why a creative won.
"""

from __future__ import annotations

from collections import defaultdict
from typing import Any, Iterable


def _num(row: dict[str, Any], key: str) -> float:
    try:
        return float(row.get(key) or 0)
    except (TypeError, ValueError):
        return 0.0


def _weighted_average(rows: list[dict[str, Any]], metric: str, weight: str = "spend") -> float:
    total_weight = sum(_num(r, weight) for r in rows)
    if not total_weight:
        return 0.0
    return sum(_num(r, metric) * _num(r, weight) for r in rows) / total_weight


def group_pattern(rows: Iterable[dict[str, Any]], field: str, *, min_spend: float = 100, min_conversions: float = 5) -> list[dict[str, Any]]:
    groups: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for row in rows:
        value = str(row.get(field) or "Unknown").strip() or "Unknown"
        groups[value].append(row)

    result = []
    for value, items in groups.items():
        spend = sum(_num(r, "spend") for r in items)
        conversions = sum(_num(r, "conversions") for r in items)
        revenue = sum(_num(r, "revenue") for r in items)
        roas = revenue / spend if spend else 0
        ctr = _weighted_average(items, "ctr")
        cpa = spend / conversions if conversions else 0
        sufficient = spend >= min_spend and conversions >= min_conversions
        result.append({
            "pattern": value,
            "field": field,
            "ad_count": len(items),
            "spend": spend,
            "conversions": conversions,
            "roas": roas,
            "ctr": ctr,
            "cpa": cpa,
            "evidence_strength": "sufficient" if sufficient else "weak",
        })
    return sorted(result, key=lambda x: (x["evidence_strength"] == "sufficient", x["roas"]), reverse=True)


def detect_winners(rows: Iterable[dict[str, Any]], *, min_spend: float = 100, min_conversions: float = 5) -> dict[str, Any]:
    rows = list(rows)
    eligible = []
    for row in rows:
        spend = _num(row, "spend")
        conversions = _num(row, "conversions")
        revenue = _num(row, "revenue")
        roas = revenue / spend if spend else _num(row, "roas")
        eligible.append({**row, "_roas": roas, "_eligible": spend >= min_spend and conversions >= min_conversions})

    qualified = [row for row in eligible if row["_eligible"]]
    top_ads = sorted(qualified, key=lambda x: x["_roas"], reverse=True)[:10]
    pattern_fields = ("hook_type", "angle", "format", "offer", "cta")
    patterns = {field: group_pattern(qualified, field, min_spend=min_spend, min_conversions=min_conversions) for field in pattern_fields}

    return {
        "qualified_ad_count": len(qualified),
        "top_ads": [
            {
                "id": row.get("id") or row.get("ad_id"),
                "name": row.get("name") or row.get("ad_name"),
                "roas": row["_roas"],
                "spend": _num(row, "spend"),
                "conversions": _num(row, "conversions"),
            }
            for row in top_ads
        ],
        "winning_patterns": patterns,
        "interpretation": "Patterns describe observed associations in the supplied dataset; they do not prove causation.",
    }
