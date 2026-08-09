"""Rule-based Meta Ads performance diagnosis.

This intentionally produces hypotheses, not claims of causation.
Input: JSON array or {"data": [...]} on stdin.
"""

from __future__ import annotations
import json, sys
from typing import Any, Dict, List


def num(row: Dict[str, Any], key: str) -> float:
    try:
        return float(row.get(key) or 0)
    except (TypeError, ValueError):
        return 0.0


def diagnose(row: Dict[str, Any]) -> Dict[str, Any]:
    spend, imp = num(row, "spend"), num(row, "impressions")
    clicks, conv = num(row, "clicks"), num(row, "conversions")
    reach = num(row, "reach")
    revenue = num(row, "revenue")
    cpm = spend / imp * 1000 if imp else 0
    ctr = clicks / imp * 100 if imp else 0
    cpc = spend / clicks if clicks else 0
    cpa = spend / conv if conv else 0
    cr = conv / clicks * 100 if clicks else 0
    roas = revenue / spend if spend else 0
    freq = imp / reach if reach else 0
    findings: List[Dict[str, str]] = []
    if imp >= 1000 and ctr < 0.8:
        findings.append({"severity": "warning", "signal": "low_ctr", "hypothesis": "Creative relevance, hook, audience fit, or placement mix may need investigation."})
    if clicks >= 100 and cr < 1.0:
        findings.append({"severity": "warning", "signal": "low_conversion_rate", "hypothesis": "Landing page, offer, checkout, tracking, or message-to-market fit may be limiting conversions."})
    if freq >= 3 and ctr > 0 and ctr < 1.0:
        findings.append({"severity": "warning", "signal": "possible_fatigue", "hypothesis": "High frequency combined with weak CTR can indicate creative fatigue; compare against historical data."})
    if spend > 0 and conv == 0:
        findings.append({"severity": "critical", "signal": "no_conversions", "hypothesis": "Check tracking, conversion event configuration, offer, landing page, and actual delivery quality before scaling."})
    if spend > 0 and revenue > 0 and roas < 1:
        findings.append({"severity": "critical", "signal": "roas_below_1", "hypothesis": "Revenue does not currently cover ad spend; investigate conversion economics and attribution before scaling."})
    return {"metrics": {"cpm": cpm, "ctr": ctr, "cpc": cpc, "cpa": cpa, "conversion_rate": cr, "roas": roas, "frequency": freq}, "findings": findings}


def main() -> None:
    data = json.load(sys.stdin)
    rows = data if isinstance(data, list) else data.get("data", [])
    json.dump([diagnose(r) for r in rows], sys.stdout, indent=2)
    sys.stdout.write("\n")


if __name__ == "__main__":
    main()
