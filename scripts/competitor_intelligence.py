"""Advanced competitor intelligence from public/browser-observed ad research.

Private spend, CPA, ROAS, targeting, and conversion data are never inferred
from public ad observations.
"""

from __future__ import annotations

from collections import Counter, defaultdict
from typing import Any, Iterable

OBSERVED_FIELDS = {
    "brand", "ad_id", "source_url", "status", "first_seen", "last_seen",
    "format", "hook", "hook_type", "primary_text", "headline", "cta", "offer",
    "offer_type", "angle", "proof", "landing_page_url", "notes",
}


def normalize_ad(ad: dict[str, Any]) -> dict[str, Any]:
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
    return {
        "total_ads": len(rows),
        "brands": dict(Counter(row.get("brand") or "Unknown" for row in rows)),
        "formats": dict(Counter(row.get("format") or "Unknown" for row in rows)),
        "angles": dict(Counter(row.get("angle") or "Unknown" for row in rows)),
        "hook_types": dict(Counter(row.get("hook_type") or "Unknown" for row in rows)),
        "ctas": dict(Counter(row.get("cta") or "Unknown" for row in rows)),
        "offers": dict(Counter(row.get("offer_type") or row.get("offer") or "None observed" for row in rows)),
    }


def creative_score(ad: dict[str, Any]) -> dict[str, Any]:
    row = normalize_ad(ad)
    components = {name: bool(row.get(name)) for name in ("hook", "offer", "cta", "proof", "angle", "primary_text")}
    return {
        "ad_id": row.get("ad_id"),
        "brand": row.get("brand"),
        "observable_creative_completeness": round(sum(components.values()) / len(components) * 10, 1),
        "components": components,
        "warning": "Content-completeness only; this is not an estimate of ROAS, CPA, spend, or profitability.",
    }


def _group_by_brand(rows: list[dict[str, Any]]) -> dict[str, list[dict[str, Any]]]:
    grouped: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for row in rows:
        grouped[str(row.get("brand") or "Unknown")].append(row)
    return grouped


def compare_brands(ads: Iterable[dict[str, Any]]) -> dict[str, Any]:
    rows = normalize_ads(ads)
    result: dict[str, Any] = {}
    for brand, brand_ads in _group_by_brand(rows).items():
        result[brand] = {
            "ad_count_observed": len(brand_ads),
            "active_count_observed": sum(str(a.get("status") or "").lower() == "active" for a in brand_ads),
            "summary": summarize(brand_ads),
            "creative_scores": [creative_score(ad) for ad in brand_ads],
        }
    return result


def recurring_patterns(ads: Iterable[dict[str, Any]], *, min_count: int = 2) -> list[dict[str, Any]]:
    rows = normalize_ads(ads)
    patterns: list[dict[str, Any]] = []
    for field in ("hook_type", "angle", "format", "offer_type", "cta"):
        for value, count in Counter(str(row.get(field) or "Unknown") for row in rows).items():
            if count >= min_count:
                patterns.append({"field": field, "pattern": value, "observed_count": count})
    return sorted(patterns, key=lambda item: item["observed_count"], reverse=True)


def analyze_brand(ads: Iterable[dict[str, Any]], brand: str) -> dict[str, Any]:
    selected = [row for row in normalize_ads(ads) if str(row.get("brand", "")).lower() == brand.lower()]
    return {
        "brand": brand,
        "observed_ads": len(selected),
        "active_count_observed": sum(str(row.get("status") or "").lower() == "active" for row in selected),
        "summary": summarize(selected),
        "first_seen": sorted(str(row["first_seen"]) for row in selected if row.get("first_seen")),
        "last_seen": sorted(str(row["last_seen"]) for row in selected if row.get("last_seen")),
    }


def market_gaps(ads: Iterable[dict[str, Any]], *, min_observed: int = 2) -> list[dict[str, Any]]:
    rows = normalize_ads(ads)
    if len(rows) < min_observed:
        return []
    gaps: list[dict[str, Any]] = []
    for field, candidates in {
        "format": ("UGC", "product demo", "education", "testimonial", "comparison"),
        "angle": ("problem-solution", "education", "comparison", "proof", "price"),
    }.items():
        counts = Counter(str(row.get(field) or "Unknown") for row in rows)
        for candidate in candidates:
            if counts.get(candidate, 0) == 0:
                gaps.append({
                    "field": field,
                    "candidate": candidate,
                    "type": "test_hypothesis",
                    "evidence": f"Not observed in the supplied {len(rows)}-ad sample.",
                    "caveat": "Does not prove the broader market lacks this pattern.",
                })
    return gaps


def competitor_report(ads: Iterable[dict[str, Any]]) -> dict[str, Any]:
    rows = normalize_ads(ads)
    return {
        "scope": "public/browser-observed competitor research",
        "summary": summarize(rows),
        "brand_comparison": compare_brands(rows),
        "recurring_patterns": recurring_patterns(rows),
        "market_gap_hypotheses": market_gaps(rows),
        "limitations": [
            "Public observations do not establish private spend, CPA, ROAS, revenue, targeting, or conversion volume.",
            "Ad presence or longevity is not proof of profitability.",
            "An unobserved pattern is not necessarily absent from the market.",
        ],
    }
