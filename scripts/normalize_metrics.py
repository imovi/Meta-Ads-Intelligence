"""Normalize common Meta Ads metrics and calculate derived KPIs."""

from __future__ import annotations
from typing import Any, Dict, Iterable, List


def _num(value: Any) -> float:
    try:
        return float(value or 0)
    except (TypeError, ValueError):
        return 0.0


def derive_metrics(row: Dict[str, Any]) -> Dict[str, Any]:
    out = dict(row)
    spend = _num(row.get("spend"))
    impressions = _num(row.get("impressions"))
    clicks = _num(row.get("clicks"))
    reach = _num(row.get("reach"))
    conversions = _num(row.get("conversions", row.get("purchases", row.get("results", 0))))
    revenue = _num(row.get("revenue", row.get("purchase_value", 0)))
    out.update({"spend": spend, "impressions": impressions, "clicks": clicks,
                "reach": reach, "conversions": conversions, "revenue": revenue})
    out["cpm"] = spend / impressions * 1000 if impressions else 0.0
    out["ctr"] = clicks / impressions * 100 if impressions else 0.0
    out["cpc"] = spend / clicks if clicks else 0.0
    out["cpa"] = spend / conversions if conversions else 0.0
    out["conversion_rate"] = conversions / clicks * 100 if clicks else 0.0
    out["roas"] = revenue / spend if spend else 0.0
    out["frequency"] = impressions / reach if reach else 0.0
    return out


def normalize(rows: Iterable[Dict[str, Any]]) -> List[Dict[str, Any]]:
    return [derive_metrics(row) for row in rows]


if __name__ == "__main__":
    import json, sys
    data = json.load(sys.stdin)
    rows = data if isinstance(data, list) else data.get("data", [])
    json.dump(normalize(rows), sys.stdout, indent=2)
    sys.stdout.write("\n")
