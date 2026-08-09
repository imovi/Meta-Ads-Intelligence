"""Creative fatigue intelligence from comparable time-series observations."""

from __future__ import annotations

from typing import Any, Iterable


def _num(row: dict[str, Any], key: str) -> float | None:
    try:
        value = row.get(key)
        return None if value is None else float(value)
    except (TypeError, ValueError):
        return None


def _pct_change(current: float | None, previous: float | None) -> float | None:
    if current is None or previous in (None, 0):
        return None
    return (current - previous) / previous * 100


def analyze_fatigue(history: Iterable[dict[str, Any]], *, ctr_drop_pct: float = 20.0, cpa_rise_pct: float = 25.0, frequency_rise_pct: float = 20.0) -> dict[str, Any]:
    """Detect a multi-signal fatigue pattern without claiming causality."""
    rows = list(history)
    if len(rows) < 3:
        return {"status": "insufficient_data", "signal": False, "confidence": "low", "reason": "At least three comparable periods are recommended."}

    first, latest = rows[0], rows[-1]
    ctr_change = _pct_change(_num(latest, "ctr"), _num(first, "ctr"))
    cpa_change = _pct_change(_num(latest, "cpa"), _num(first, "cpa"))
    freq_change = _pct_change(_num(latest, "frequency"), _num(first, "frequency"))
    conversion_change = _pct_change(_num(latest, "conversions"), _num(first, "conversions"))

    signals = {
        "ctr_decline": ctr_change is not None and ctr_change <= -abs(ctr_drop_pct),
        "cpa_increase": cpa_change is not None and cpa_change >= abs(cpa_rise_pct),
        "frequency_increase": freq_change is not None and freq_change >= abs(frequency_rise_pct),
        "conversion_decline": conversion_change is not None and conversion_change <= -abs(ctr_drop_pct),
    }
    count = sum(signals.values())
    detected = count >= 2
    confidence = "high" if count >= 3 else "medium" if count == 2 else "low"

    recommendation = []
    if detected:
        recommendation = [
            "Review the creative against recent frequency and audience saturation.",
            "Test a materially different opening hook or visual while preserving the strongest proven message where possible.",
            "Compare the new variation against the fatigued creative using a defined success metric and sufficient sample size.",
        ]
    else:
        recommendation = ["Continue monitoring comparable periods; do not declare fatigue from a single weak metric."]

    return {
        "status": "likely_fatigue_signal" if detected else "no_clear_fatigue_signal",
        "signal": detected,
        "confidence": confidence,
        "signals": signals,
        "changes": {
            "ctr_pct": ctr_change,
            "cpa_pct": cpa_change,
            "frequency_pct": freq_change,
            "conversions_pct": conversion_change,
        },
        "recommendations": recommendation,
        "note": "Fatigue is a diagnostic hypothesis. Validate audience size, delivery, seasonality, tracking, placement mix, and offer before attributing causality to creative fatigue.",
    }


def compare_variations(variations: Iterable[dict[str, Any]], *, min_conversions: float = 5) -> list[dict[str, Any]]:
    """Compare current creative variants and flag weak evidence."""
    result = []
    for row in variations:
        conversions = _num(row, "conversions") or 0
        spend = _num(row, "spend") or 0
        result.append({
            **row,
            "evidence_strength": "sufficient" if conversions >= min_conversions and spend > 0 else "weak",
            "status": "candidate" if conversions >= min_conversions and spend > 0 else "collect_more_data",
        })
    return sorted(result, key=lambda x: (x["evidence_strength"] == "sufficient", float(x.get("roas") or 0)), reverse=True)
