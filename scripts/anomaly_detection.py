"""Conservative anomaly detection for Meta Ads performance data.

Detects changes in supplied comparable periods. It reports signals and does not
claim causation. Thresholds are configurable rather than universal truths.
"""

from __future__ import annotations

from typing import Any, Iterable


def _num(row: dict[str, Any], key: str) -> float | None:
    value = row.get(key)
    if value is None:
        return None
    try:
        return float(value)
    except (TypeError, ValueError):
        return None


def percent_change(current: float | None, baseline: float | None) -> float | None:
    if current is None or baseline in (None, 0):
        return None
    return (current - baseline) / baseline * 100


def detect_period_anomalies(
    current: dict[str, Any],
    baseline: dict[str, Any],
    *,
    pct_threshold: float = 25.0,
    absolute_ctr_threshold: float = 0.5,
) -> list[dict[str, Any]]:
    """Return material metric movements with conservative defaults."""
    findings: list[dict[str, Any]] = []
    checks = (
        ("cpa", "increase", True),
        ("roas", "decrease", True),
        ("ctr", "decrease", False),
        ("cpm", "increase", True),
        ("frequency", "increase", True),
        ("conversions", "decrease", True),
        ("spend", "increase", True),
    )

    for metric, direction, use_pct in checks:
        now = _num(current, metric)
        old = _num(baseline, metric)
        change = percent_change(now, old)
        if now is None or old is None:
            continue
        triggered = False
        if metric == "ctr":
            triggered = (old - now) >= absolute_ctr_threshold
        elif change is not None:
            triggered = change >= pct_threshold if direction == "increase" else change <= -pct_threshold
        if triggered:
            findings.append({
                "metric": metric,
                "direction": direction,
                "current": now,
                "baseline": old,
                "percent_change": change,
                "signal": "anomaly",
                "confidence": "screening",
                "note": "Investigate context before attributing cause.",
            })
    return findings


def detect_tracking_anomaly(current: dict[str, Any]) -> list[str]:
    """Flag simple impossible/inconsistent values in supplied data."""
    issues: list[str] = []
    spend = _num(current, "spend")
    conversions = _num(current, "conversions")
    clicks = _num(current, "clicks")
    impressions = _num(current, "impressions")
    revenue = _num(current, "revenue")

    if spend is not None and spend < 0:
        issues.append("Spend is negative.")
    if conversions is not None and conversions < 0:
        issues.append("Conversions are negative.")
    if clicks is not None and impressions is not None and clicks > impressions:
        issues.append("Clicks exceed impressions; verify source fields or aggregation.")
    if revenue is not None and revenue < 0:
        issues.append("Revenue is negative; verify refunds/adjustments and source semantics.")
    return issues


def scan(rows: Iterable[dict[str, Any]], *, pct_threshold: float = 25.0) -> list[dict[str, Any]]:
    """Scan chronological rows against the immediately previous comparable row."""
    items = list(rows)
    results: list[dict[str, Any]] = []
    for index in range(1, len(items)):
        current = items[index]
        baseline = items[index - 1]
        results.extend(detect_period_anomalies(current, baseline, pct_threshold=pct_threshold))
        tracking = detect_tracking_anomaly(current)
        if tracking:
            results.append({"metric": "data_integrity", "signal": "warning", "issues": tracking})
    return results
