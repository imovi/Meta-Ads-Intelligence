"""Normalize and score public competitor ad observations.

This module intentionally works only on supplied/public observations. It does
not scrape private Ads Manager data and never invents spend, CPA, ROAS, or
exact targeting.
"""

from __future__ import annotations

from collections import Counter
from typing import Any, Iterable


OBSERVED_FIELDS = {
    "brand", "ad_id", "source_url", "status", "first_seen", "last_seen",
    "format", "hook", "primary_text", "headline", "cta", "offer", "angle",
    "proof", "landing_page_url", "notes",
}


def normalize_ad(ad: dict[str, Any]) -> dict[str, Any]:
    """Return a predictable public-observation record."""
    normalized = {key: ad.get(key) for key in OBSERVED_FIELDS}
    normalized["brand"] = normalized.get("brand") or "Unknown"
    normalized["evidence"] = ad.get("evidence", "Observed")
    if normalized["evidence"] not in {"Observed", "Inferred", "Unknown"}:
        normalized["evidence"] = "Unknown"
    return normalized


def normalize_ads(ads: Iterable[dict[str, Any]]) -> list[dict[str, Any]]:
    return [normalize_ad(ad) for ad in ads]


def summarize(ads: Iterable[dict[str, Any]]) -> dict[str, Any]:
    rows = normalize_ads(ads)
    formats = Counter((row.get("format") or "Unknown") for row in rows)
    angles = Counter((row.get("angle") or "Unknown") for row in rows)
    ctas = Counter((row.get("cta") or "Unknown") for row in rows)
    offers = Counter((row.get("offer") or "None observed") for row in rows)
    brands = Counter((row.get("brand") or "Unknown") for row in rows)
    return {
        "total_ads": len(rows),
        "brands": dict(brands),
        "formats": dict(formats),
        "angles": dict(angles),
        "ctas": dict(ctas),
        "offers": dict(offers),
    }


def creative_score(ad: dict[str, Any]) -> dict[str, Any]:
    """Score observable creative completeness, not business performance."""
    row = normalize_ad(ad)
    components = {
        "hook": bool(row.get("hook")),
        "offer": bool(row.get("offer")),
        "cta": bool(row.get("cta")),
        "proof": bool(row.get("proof")),
        "angle": bool(row.get("angle")),
        "primary_text": bool(row.get("primary_text")),
    }
    score = round(sum(components.values()) / len(components) * 10, 1)
    return {
        "ad_id": row.get("ad_id"),
        "brand": row.get("brand"),
        "observable_creative_completeness": score,
        "components": components,
        "warning": "This is a content-completeness score, not an estimate of ROAS, CPA, spend, or ad profitability.",
    }


def compare_brands(ads: Iterable[dict[str, Any]]) -> dict[str, Any]:
    rows = normalize_ads(ads)
    by_brand: dict[str, list[dict[str, Any]]] = {}
    for row in rows:
        by_brand.setdefault(row["brand"], []).append(row)

    result: dict[str, Any] = {}
    for brand, brand_ads in by_brand.items():
        summary = summarize(brand_ads)
        result[brand] = {
            "ad_count_observed": summary["total_ads"],
            "formats": summary["formats"],
            "angles": summary["angles"],
            "ctas": summary["ctas"],
            "offers": summary["offers"],
            "creative_scores": [creative_score(ad) for ad in brand_ads],
        }
    return result


def market_gaps(ads: Iterable[dict[str, Any]]) -> list[str]:
    """Identify simple observable gaps; these are hypotheses for testing."""
    rows = normalize_ads(ads)
    if not rows:
        return []
    gaps: list[str] = []
    if not any(row.get("proof") for row in rows):
        gaps.append("No observable social-proof element was captured; test credible proof as a differentiated angle.")
    if not any(row.get("offer") for row in rows):
        gaps.append("No explicit offer was captured; test value/offer messaging if appropriate to the product.")
    formats = {row.get("format") for row in rows if row.get("format")}
    if len(formats) == 1:
        gaps.append(f"Observed creative format is concentrated in {next(iter(formats))}; test a distinct format as a hypothesis.")
    return gaps
