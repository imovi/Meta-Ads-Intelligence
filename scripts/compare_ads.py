"""Compare Meta Ads rows using a transparent, evidence-aware score.

The score is a decision aid, not a claim that one ad is statistically superior.
"""

from __future__ import annotations
import json, sys
from typing import Any, Dict, List


def n(v: Any) -> float:
    try: return float(v or 0)
    except (TypeError, ValueError): return 0.0


def compare(rows: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    if not rows: return []
    enriched = []
    for r in rows:
        spend, imp, clicks, conv, revenue = map(n, [r.get("spend"), r.get("impressions"), r.get("clicks"), r.get("conversions", r.get("purchases", 0)), r.get("revenue", 0)])
        ctr = clicks / imp * 100 if imp else 0
        cpa = spend / conv if conv else None
        roas = revenue / spend if spend else None
        # Score rewards outcome quality but discounts very small samples.
        evidence = min(1.0, (spend / 100.0) ** 0.5) if spend else 0.0
        outcome = (min(2.0, roas) / 2.0 if roas is not None else 0.0)
        click_signal = min(1.0, ctr / 2.0)
        score = (0.65 * outcome + 0.35 * click_signal) * evidence * 100
        item = dict(r)
        item.update({"ctr": ctr, "cpa": cpa, "roas": roas, "evidence_strength": evidence, "decision_score": score})
        enriched.append(item)
    return sorted(enriched, key=lambda x: x["decision_score"], reverse=True)


if __name__ == "__main__":
    data = json.load(sys.stdin)
    rows = data if isinstance(data, list) else data.get("data", [])
    json.dump(compare(rows), sys.stdout, indent=2)
    sys.stdout.write("\n")
