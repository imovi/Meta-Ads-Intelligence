"""Budget allocation simulator for Meta Ads recommendations.

Analysis-only: it proposes allocations and never writes to an ad account.
"""

from __future__ import annotations

from typing import Any, Iterable


def _num(row: dict[str, Any], key: str) -> float:
    try:
        return float(row.get(key) or 0)
    except (TypeError, ValueError):
        return 0.0


def classify_campaign(row: dict[str, Any], *, target_cpa: float | None = None, target_roas: float | None = None) -> str:
    roas = _num(row, "roas")
    cpa = _num(row, "cpa")
    conversions = _num(row, "conversions")
    fatigue = bool(row.get("fatigue_signal"))
    if fatigue:
        return "test"
    if target_roas and roas >= target_roas and conversions >= 5:
        return "scale"
    if target_cpa and cpa > target_cpa and conversions >= 5:
        return "reduce"
    if target_roas and roas < target_roas and conversions < 5:
        return "test"
    return "hold"


def simulate_allocation(rows: Iterable[dict[str, Any]], total_budget: float, *, target_cpa: float | None = None, target_roas: float | None = None, test_budget_pct: float = 10.0) -> dict[str, Any]:
    rows = list(rows)
    if total_budget <= 0:
        raise ValueError("total_budget must be greater than zero")
    if not 0 <= test_budget_pct <= 50:
        raise ValueError("test_budget_pct must be between 0 and 50")

    classified = [{**row, "recommendation": classify_campaign(row, target_cpa=target_cpa, target_roas=target_roas)} for row in rows]
    scales = [r for r in classified if r["recommendation"] == "scale"]
    holds = [r for r in classified if r["recommendation"] == "hold"]
    reduces = [r for r in classified if r["recommendation"] == "reduce"]
    tests = [r for r in classified if r["recommendation"] == "test"]

    test_pool = total_budget * test_budget_pct / 100
    deploy_pool = total_budget - test_pool

    scale_weight = sum(max(_num(r, "roas"), 0.1) * max(_num(r, "conversions"), 1) for r in scales)
    hold_weight = sum(max(_num(r, "conversions"), 1) for r in holds)
    deploy_weight = scale_weight + hold_weight

    allocations = []
    for row in classified:
        if row["recommendation"] == "scale" and deploy_weight:
            budget = deploy_pool * (max(_num(row, "roas"), 0.1) * max(_num(row, "conversions"), 1)) / deploy_weight
        elif row["recommendation"] == "hold" and deploy_weight:
            budget = deploy_pool * max(_num(row, "conversions"), 1) / deploy_weight
        elif row["recommendation"] == "test" and tests:
            budget = test_pool / len(tests)
        else:
            budget = 0.0
        allocations.append({"id": row.get("id") or row.get("campaign_id"), "name": row.get("name") or row.get("campaign_name"), "recommendation": row["recommendation"], "proposed_daily_budget": round(budget, 2)})

    return {
        "total_budget": total_budget,
        "test_pool": round(test_pool, 2),
        "allocations": allocations,
        "summary": {"scale": len(scales), "hold": len(holds), "reduce": len(reduces), "test": len(tests)},
        "method": "directional evidence-weighted simulation; not a forecast or guaranteed outcome",
        "action_allowed": False,
    }
