"""Natural-language intent router for Meta Ads Intelligence.

The router maps user language to a safe skill mode. It does not execute actions
and never infers permission to modify an ad account.
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class Route:
    mode: str
    confidence: str
    reason: str
    action_requested: bool = False
    confirmation_required: bool = False


MODE_PATTERNS: dict[str, tuple[str, ...]] = {
    "action": (
        r"\b(pause|resume|activate|enable|disable|delete|remove|publish|create|launch|duplicate|increase|decrease|change|update|edit|set)\b",
        r"\b(budget|campaign|ad set|ad|targeting|bid|placement)\b.*\b(to|change|set|pause|resume|delete|create)\b",
    ),
    "audit": (r"\b(full|complete|account)\b.*\b(audit|checkup|health check)\b", r"\baudit (my )?(meta|facebook|instagram) ads\b"),
    "competitor": (r"\bcompetitor(s)?\b", r"\bad library\b", r"\bwhat (is|are) .* running\b"),
    "creative": (r"\bcreative(s)?\b", r"\bhook(s)?\b", r"\b(reel|video|image) ad\b", r"\bad copy\b"),
    "report": (r"\b(report|weekly report|monthly report|daily report)\b", r"\bsummar(y|ize)\b.*\bads\b"),
    "monitor": (r"\b(monitor|alert|watch|anomaly|spike|drop)\b", r"\bnotify\b.*\b(cpa|roas|ads)\b"),
    "strategy": (r"\b(strategy|optimi[sz]e|scale|scaling|budget allocation|next 7 days)\b", r"\bwhat should (i|we) do\b"),
    "analyze": (r"\b(analy[sz]e|analysis|check|performance|why|compare)\b", r"\b(cpa|roas|ctr|cpc|cpm|conversion)\b"),
}


def _matches(text: str, patterns: tuple[str, ...]) -> bool:
    return any(re.search(pattern, text, re.IGNORECASE) for pattern in patterns)


def route(text: str) -> Route:
    normalized = " ".join(text.strip().split())
    if not normalized:
        return Route("analyze", "low", "No command supplied; default to analysis.")

    # Explicit action language has priority over analysis words.
    if _matches(normalized, MODE_PATTERNS["action"]):
        return Route(
            "action",
            "high",
            "Explicit account-changing language detected.",
            action_requested=True,
            confirmation_required=True,
        )

    priority = ["audit", "competitor", "creative", "report", "monitor", "strategy", "analyze"]
    for mode in priority:
        if _matches(normalized, MODE_PATTERNS[mode]):
            return Route(mode, "high", f"Matched {mode} task language.")

    return Route("analyze", "low", "No specialized intent detected; safe default is analysis.")


def explain_route(text: str) -> dict[str, Any]:
    result = route(text)
    return {
        "mode": result.mode,
        "confidence": result.confidence,
        "reason": result.reason,
        "action_requested": result.action_requested,
        "confirmation_required": result.confirmation_required,
        "safe_default": "analysis",
    }
