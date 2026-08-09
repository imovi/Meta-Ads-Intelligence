"""Scaling intelligence: decide whether a campaign is ready to scale, hold, reduce, or test.

Analysis-only. No Meta account writes are performed here.
"""
from __future__ import annotations
from typing import Any, Iterable


def _num(row: dict[str, Any], key: str) -> float | None:
    try:
        v = row.get(key)
        return None if v is None else float(v)
    except (TypeError, ValueError):
        return None


def _score(row: dict[str, Any], *, target_cpa: float | None, target_roas: float | None) -> tuple[int, list[str]]:
    score = 0
    evidence: list[str] = []
    conversions = _num(row, "conversions") or 0
    roas = _num(row, "roas")
    cpa = _num(row, "cpa")
    trend = _num(row, "roas_trend_pct")
    freq = _num(row, "frequency")
    ctr_trend = _num(row, "ctr_trend_pct")
    fatigue = bool(row.get("fatigue_signal"))

    if conversions >= 10:
        score += 2; evidence.append("meaningful conversion volume")
    elif conversions >= 5:
        score += 1; evidence.append("some conversion volume")
    else:
        evidence.append("limited conversion volume")

    if target_roas is not None and roas is not None:
        if roas >= target_roas * 1.15:
            score += 2; evidence.append("ROAS materially above target")
        elif roas >= target_roas:
            score += 1; evidence.append("ROAS meets target")
        else:
            score -= 2; evidence.append("ROAS below target")

    if target_cpa is not None and cpa is not None:
        if cpa <= target_cpa * 0.85:
            score += 2; evidence.append("CPA materially below target")
        elif cpa <= target_cpa:
            score += 1; evidence.append("CPA meets target")
        else:
            score -= 2; evidence.append("CPA above target")

    if trend is not None:
        if trend >= 10:
            score += 1; evidence.append("positive ROAS trend")
        elif trend <= -15:
            score -= 2; evidence.append("negative ROAS trend")

    if ctr_trend is not None and ctr_trend <= -20:
        score -= 1; evidence.append("CTR declining materially")

    if fatigue:
        score -= 2; evidence.append("creative fatigue signal")
    if freq is not None and freq >= 4:
        score -= 1; evidence.append("high frequency requires scrutiny")

    return score, evidence


def assess_scaling(row: dict[str, Any], *, target_cpa: float | None = None, target_roas: float | None = None) -> dict[str, Any]:
    score, evidence = _score(row, target_cpa=target_cpa, target_roas=target_roas)
    conversions = _num(row, "conversions") or 0
    if score >= 5 and conversions >= 10:
        recommendation, risk = "scale", "low_to_medium"
    elif score >= 2:
        recommendation, risk = "hold", "medium"
    elif conversions < 5:
        recommendation, risk = "test", "high"
    else:
        recommendation, risk = "reduce", "medium_to_high"
    return {
        "id": row.get("id") or row.get("campaign_id"),
        "name": row.get("name") or row.get("campaign_name") or "Unknown",
        "recommendation": recommendation,
        "risk": risk,
        "score": score,
        "evidence": evidence,
        "action_allowed": False,
        "note": "Scaling readiness is a decision-support signal, not a guarantee of future performance.",
    }


def assess_account(rows: Iterable[dict[str, Any]], *, target_cpa: float | None = None, target_roas: float | None = None) -> list[dict[str, Any]]:
    results = [assess_scaling(r, target_cpa=target_cpa, target_roas=target_roas) for r in rows]
    order = {"scale": 0, "hold": 1, "test": 2, "reduce": 3}
    return sorted(results, key=lambda x: (order[x["recommendation"]], -x["score"]))
