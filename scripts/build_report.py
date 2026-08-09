"""Build a compact Markdown Meta Ads report from normalized JSON rows."""

from __future__ import annotations
import json, sys
from typing import Any, Dict, List


def n(v: Any) -> float:
    try: return float(v or 0)
    except (TypeError, ValueError): return 0.0


def report(rows: List[Dict[str, Any]]) -> str:
    spend = sum(n(r.get("spend")) for r in rows)
    revenue = sum(n(r.get("revenue", r.get("purchase_value"))) for r in rows)
    impressions = sum(n(r.get("impressions")) for r in rows)
    clicks = sum(n(r.get("clicks")) for r in rows)
    conversions = sum(n(r.get("conversions", r.get("purchases", 0))) for r in rows)
    cpm = spend / impressions * 1000 if impressions else 0
    ctr = clicks / impressions * 100 if impressions else 0
    cpc = spend / clicks if clicks else 0
    cpa = spend / conversions if conversions else 0
    roas = revenue / spend if spend else 0
    lines = ["# Meta Ads Performance Report", "", "## Executive Summary", f"- Spend: {spend:.2f}", f"- Revenue: {revenue:.2f}", f"- Conversions: {conversions:.0f}", f"- ROAS: {roas:.2f}x", "", "## KPI Summary", "| KPI | Value |", "|---|---:|", f"| CPM | {cpm:.2f} |", f"| CTR | {ctr:.2f}% |", f"| CPC | {cpc:.2f} |", f"| CPA | {cpa:.2f} |", f"| ROAS | {roas:.2f}x |", "", "## Notes", "- Treat diagnosis as evidence-based hypotheses; verify attribution and tracking before making major decisions."]
    return "\n".join(lines) + "\n"


if __name__ == "__main__":
    data = json.load(sys.stdin)
    rows = data if isinstance(data, list) else data.get("data", [])
    sys.stdout.write(report(rows))
