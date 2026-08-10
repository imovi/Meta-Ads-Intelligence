"""Generate controlled creative test hypotheses from observed winners/fatigue signals."""

from __future__ import annotations

from typing import Any, Iterable


def _text(value: Any) -> str:
    return str(value or "").strip()


def generate_hook_variations(base_hook: str, count: int = 5) -> list[str]:
    """Generate test directions, not claims of guaranteed performance."""
    base = _text(base_hook) or "the core customer problem"
    templates = [
        f"Problem-first: make the pain point explicit around {base}.",
        f"Outcome-first: lead with the desired result connected to {base}.",
        f"Curiosity: open with a question that challenges the assumption behind {base}.",
        f"Demonstration: show the product/result immediately before explaining {base}.",
        f"Proof-first: open with a concise customer/result proof related to {base}.",
    ]
    return templates[:max(0, count)]


def generate_creative_tests(winner: dict[str, Any], *, fatigue: dict[str, Any] | None = None, count: int = 5) -> list[dict[str, Any]]:
    """Create isolated-variable hypotheses from a winning creative."""
    hook = _text(winner.get("hook")) or _text(winner.get("hook_type")) or "the proven hook"
    body = _text(winner.get("copy"))
    offer = _text(winner.get("offer"))
    cta = _text(winner.get("cta")) or "the existing CTA"
    format_name = _text(winner.get("format")) or "existing format"

    ideas = [
        {"name": "Hook test", "change": "hook", "concept": generate_hook_variations(hook, 1)[0], "keep": ["body", "offer", "CTA", "format"]},
        {"name": "Opening visual test", "change": "opening_visual", "concept": "Replace the first visual with an immediate product/result demonstration.", "keep": ["hook", "body", "offer", "CTA"]},
        {"name": "Proof test", "change": "proof", "concept": "Replace/add a specific testimonial or demonstration proof while keeping the core promise.", "keep": ["hook", "body", "offer", "CTA"]},
        {"name": "Offer framing test", "change": "offer_framing", "concept": f"Test a clearer value/offer presentation around {offer or 'the current offer'}.", "keep": ["hook", "body", "proof", "CTA"]},
        {"name": "CTA test", "change": "cta", "concept": f"Test a more intent-matched CTA instead of {cta}.", "keep": ["hook", "body", "offer", "format"]},
    ]

    if fatigue and fatigue.get("signal"):
        ideas.append({"name": "Fatigue reset", "change": "angle", "concept": "Create a materially different angle/format while retaining the strongest validated product promise.", "keep": ["product", "core_benefit"]})

    selected = ideas[:max(0, count)]
    for index, idea in enumerate(selected, start=1):
        idea["test_id"] = f"T{index:02d}"
        idea["control"] = {"format": format_name, "body": body, "offer": offer, "cta": cta}
        idea["hypothesis"] = "The changed variable may improve the selected success metric while the retained variables reduce confounding."
        idea["success_metric"] = "Choose before launch: CTR, CPA, ROAS, or conversion rate based on the business objective."
        idea["stop_condition"] = "Define a minimum spend/conversion sample and a decision threshold before judging the test."
    return selected


def build_ab_matrix(winner: dict[str, Any], *, fatigue: dict[str, Any] | None = None, count: int = 5) -> dict[str, Any]:
    tests = generate_creative_tests(winner, fatigue=fatigue, count=count)
    return {
        "control": {
            "id": winner.get("id") or winner.get("ad_id"),
            "name": winner.get("name") or winner.get("ad_name") or "Control",
        },
        "tests": tests,
        "method": "one_primary_variable_at_a_time",
        "warning": "These are hypotheses. They do not guarantee improved performance and should be evaluated with sufficient sample size.",
    }
