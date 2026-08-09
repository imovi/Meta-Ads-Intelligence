"""Deep single-ad analysis from browser observations and performance data."""

from __future__ import annotations

from typing import Any


def _num(row: dict[str, Any], key: str) -> float | None:
    try:
        value = row.get(key)
        return None if value is None else float(value)
    except (TypeError, ValueError):
        return None


def score_dimension(value: Any, *, strong: set[str], weak: set[str]) -> str:
    if isinstance(value, (int, float)):
        if value >= 8:
            return "strong"
        if value <= 4:
            return "weak"
        return "moderate"
    text = str(value or "").strip().lower()
    if text in strong:
        return "strong"
    if text in weak:
        return "weak"
    return "unknown"


def analyze_ad(ad: dict[str, Any], *, baseline: dict[str, Any] | None = None) -> dict[str, Any]:
    """Return structured analysis; does not invent missing creative observations."""
    dimensions = {
        "hook": score_dimension(ad.get("hook_score"), strong={"strong"}, weak={"weak"}),
        "offer": score_dimension(ad.get("offer_score"), strong={"strong"}, weak={"weak"}),
        "proof": score_dimension(ad.get("proof_score"), strong={"strong"}, weak={"weak"}),
        "cta": score_dimension(ad.get("cta_score"), strong={"strong"}, weak={"weak"}),
        "visual": score_dimension(ad.get("visual_score"), strong={"strong"}, weak={"weak"}),
    }

    findings: list[dict[str, Any]] = []
    ctr = _num(ad, "ctr")
    cpc = _num(ad, "cpc")
    cpa = _num(ad, "cpa")
    roas = _num(ad, "roas")

    if ctr is not None:
        findings.append({"type": "performance", "metric": "ctr", "value": ctr, "interpretation": "traffic response signal; compare with account baseline"})
    if cpc is not None:
        findings.append({"type": "performance", "metric": "cpc", "value": cpc, "interpretation": "click efficiency signal; compare with comparable ads"})
    if cpa is not None:
        findings.append({"type": "performance", "metric": "cpa", "value": cpa, "interpretation": "conversion efficiency signal; check conversion volume"})
    if roas is not None:
        findings.append({"type": "performance", "metric": "roas", "value": roas, "interpretation": "revenue efficiency signal; validate attribution"})

    if baseline:
        for metric in ("ctr", "cpc", "cpa", "roas"):
            current = _num(ad, metric)
            old = _num(baseline, metric)
            if current is not None and old not in (None, 0):
                change = (current - old) / old * 100
                findings.append({"type": "comparison", "metric": metric, "percent_change": change, "interpretation": "directional comparison; investigate context"})

    missing = [key for key in ("hook", "copy", "offer", "proof", "cta", "format") if not ad.get(key)]
    return {
        "id": ad.get("id") or ad.get("ad_id"),
        "name": ad.get("name") or ad.get("ad_name") or "Unknown",
        "dimensions": dimensions,
        "findings": findings,
        "missing_observations": missing,
        "source": ad.get("source", "unknown"),
        "confidence": "high" if not missing else "limited_by_missing_creative_observations",
        "next_questions": [
            "Does the first 1–3 seconds communicate the core problem or benefit?",
            "Is the offer understandable without extra context?",
            "Is the proof credible and specific?",
            "Does the CTA match the user's intent and landing-page message?",
        ],
    }
