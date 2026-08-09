"""Orchestrate a browser-first public research plan.

This module plans and structures research; the host browser agent performs
navigation. It never assumes access to private competitor performance data.
"""

from __future__ import annotations

from typing import Any


RESEARCH_STEPS = (
    "identify_subject",
    "collect_public_ad_observations",
    "inspect_creative_patterns",
    "inspect_offers_and_copy",
    "inspect_public_destination_pages",
    "compare_competitors",
    "identify_market_gaps",
    "generate_testable_opportunities",
    "produce_research_report",
)


def build_research_plan(subject: str, *, competitors: list[str] | None = None, market: str | None = None, product: str | None = None) -> dict[str, Any]:
    return {
        "subject": subject,
        "competitors": competitors or [],
        "market": market,
        "product": product,
        "steps": list(RESEARCH_STEPS),
        "browser_preferred": True,
        "api_required": False,
        "private_data_allowed": False,
        "deliverables": [
            "research scope",
            "public evidence log",
            "competitor creative patterns",
            "offer and messaging patterns",
            "public landing-page observations",
            "market-gap hypotheses",
            "creative opportunities",
            "recommended tests",
            "confidence and limitations",
        ],
    }


def record_observation(observations: list[dict[str, Any]], *, source: str, subject: str, finding: str, url: str | None = None, evidence_type: str = "observed") -> list[dict[str, Any]]:
    if evidence_type not in {"observed", "inferred", "unknown"}:
        raise ValueError("evidence_type must be observed, inferred, or unknown")
    item = {
        "source": source,
        "subject": subject,
        "finding": finding,
        "evidence_type": evidence_type,
    }
    if url:
        item["url"] = url
    return [*observations, item]


def summarize_research(plan: dict[str, Any], observations: list[dict[str, Any]]) -> dict[str, Any]:
    counts = {key: sum(1 for item in observations if item.get("evidence_type") == key) for key in ("observed", "inferred", "unknown")}
    return {
        "subject": plan["subject"],
        "observation_count": len(observations),
        "evidence_counts": counts,
        "observations": observations,
        "limitations": [
            "Public ad research does not reveal competitor private spend, CPA, ROAS, targeting, conversion volume, or internal account decisions unless independently supplied.",
            "Absence from the observed sample does not prove absence from the broader market.",
            "Browser availability and login state depend on the host agent.",
        ],
    }
