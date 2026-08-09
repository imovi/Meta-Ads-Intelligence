"""Creative analysis utilities for Meta Ads Intelligence.

The module analyzes observable creative structure and performance signals. It
never treats a creative score as proof of business performance.
"""

from __future__ import annotations

from typing import Any, Iterable


COMPONENTS = ("hook", "problem", "solution", "benefit", "proof", "offer", "objection", "cta")


def analyze_copy(ad: dict[str, Any]) -> dict[str, Any]:
    """Break ad copy into observable components supplied by the caller."""
    text = " ".join(str(ad.get(k) or "") for k in ("primary_text", "headline", "description"))
    return {
        "hook": ad.get("hook"),
        "problem": ad.get("problem"),
        "solution": ad.get("solution"),
        "benefit": ad.get("benefit"),
        "proof": ad.get("proof"),
        "offer": ad.get("offer"),
        "objection": ad.get("objection"),
        "cta": ad.get("cta"),
        "text_length": len(text),
        "has_hook": bool(ad.get("hook")),
        "has_cta": bool(ad.get("cta")),
    }


def creative_completeness(ad: dict[str, Any]) -> dict[str, Any]:
    components = {name: bool(ad.get(name)) for name in COMPONENTS}
    present = sum(components.values())
    score = round((present / len(COMPONENTS)) * 10, 1)
    return {
        "score": score,
        "components_present": present,
        "components_total": len(COMPONENTS),
        "components": components,
        "interpretation": "Observable message completeness only; not a prediction of ROAS, CPA, or profitability.",
    }


def classify_hook(ad: dict[str, Any]) -> str:
    """Use explicit caller-provided hook_type when available."""
    return str(ad.get("hook_type") or "Unclassified")


def fatigue_signal(history: Iterable[dict[str, Any]]) -> dict[str, Any]:
    """Detect a simple multi-period fatigue pattern from supplied metrics.

    Requires chronological rows containing CTR and optionally frequency/CPA.
    This is a signal, not a causal conclusion.
    """
    rows = list(history)
    if len(rows) < 2:
        return {"status": "insufficient_data", "signal": False, "reason": "Need at least two comparable periods."}

    first, last = rows[0], rows[-1]
    try:
        ctr_change = float(last.get("ctr", 0)) - float(first.get("ctr", 0))
    except (TypeError, ValueError):
        return {"status": "invalid_data", "signal": False, "reason": "CTR values must be numeric."}

    frequency_rising = False
    if first.get("frequency") is not None and last.get("frequency") is not None:
        frequency_rising = float(last["frequency"]) > float(first["frequency"])

    cpa_rising = False
    if first.get("cpa") is not None and last.get("cpa") is not None:
        cpa_rising = float(last["cpa"]) > float(first["cpa"])

    signal = ctr_change < 0 and (frequency_rising or cpa_rising)
    return {
        "status": "signal_detected" if signal else "no_clear_signal",
        "signal": signal,
        "ctr_change": round(ctr_change, 4),
        "frequency_rising": frequency_rising,
        "cpa_rising": cpa_rising,
        "interpretation": "Possible creative fatigue; validate with spend, conversion volume, audience size, and other delivery context.",
    }


def rank_creatives(rows: Iterable[dict[str, Any]]) -> list[dict[str, Any]]:
    """Rank supplied creatives by business metrics when available.

    Requires at least one meaningful outcome metric. Small samples are flagged.
    """
    items = []
    for row in rows:
        spend = float(row.get("spend") or 0)
        conversions = float(row.get("conversions") or 0)
        roas = row.get("roas")
        if roas is not None:
            score = float(roas)
            metric = "roas"
        elif conversions > 0 and spend > 0:
            score = conversions / spend
            metric = "conversions_per_spend"
        else:
            score = 0
            metric = "insufficient_outcome_data"
        item = dict(row)
        item["decision_score"] = score
        item["decision_metric"] = metric
        item["sample_warning"] = spend < 50 or conversions < 5
        items.append(item)
    return sorted(items, key=lambda x: x["decision_score"], reverse=True)
