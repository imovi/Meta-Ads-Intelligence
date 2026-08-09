"""Import and normalize common Meta Ads export/API-shaped datasets.

Supported inputs are CSV text, JSON text, or already-loaded Python rows. The
normalizer maps common column aliases into the internal schema while preserving
unknown fields for downstream analysis.
"""

from __future__ import annotations

import csv
import io
import json
from typing import Any, Iterable


ALIASES = {
    "campaign_name": {"campaign name", "campaign_name", "campaign"},
    "adset_name": {"ad set name", "adset name", "adset_name", "ad set"},
    "ad_name": {"ad name", "ad_name", "ad"},
    "spend": {"amount spent", "spend", "cost", "amount_spent"},
    "impressions": {"impressions", "impression"},
    "reach": {"reach"},
    "clicks": {"clicks", "link clicks", "link_clicks", "outbound clicks"},
    "ctr": {"ctr", "link ctr", "link_ctr"},
    "cpc": {"cpc", "cost per click", "cost_per_click"},
    "cpm": {"cpm", "cost per 1,000 impressions"},
    "conversions": {"conversions", "purchases", "results", "website purchases"},
    "revenue": {"revenue", "purchase conversion value", "purchase_conversion_value", "value"},
    "date_start": {"date", "date start", "date_start", "reporting starts"},
    "date_stop": {"date stop", "date_stop", "reporting ends"},
    "frequency": {"frequency"},
}


def _key(value: Any) -> str:
    return " ".join(str(value or "").strip().lower().replace("_", " ").split())


def _find_canonical(raw_key: str) -> str | None:
    normalized = _key(raw_key)
    for canonical, aliases in ALIASES.items():
        if normalized in aliases:
            return canonical
    return None


def _number(value: Any) -> Any:
    if value is None or value == "":
        return None
    if isinstance(value, (int, float)):
        return value
    text = str(value).strip().replace(",", "").replace("%", "")
    try:
        return float(text)
    except ValueError:
        return value


def normalize_row(row: dict[str, Any]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for raw_key, value in row.items():
        canonical = _find_canonical(raw_key)
        result[canonical or raw_key] = _number(value) if canonical in {
            "spend", "impressions", "reach", "clicks", "ctr", "cpc", "cpm", "conversions", "revenue", "frequency"
        } else value
    return result


def normalize_rows(rows: Iterable[dict[str, Any]]) -> list[dict[str, Any]]:
    return [normalize_row(row) for row in rows]


def load_csv(text: str) -> list[dict[str, Any]]:
    return normalize_rows(csv.DictReader(io.StringIO(text)))


def load_json(text: str) -> list[dict[str, Any]]:
    data = json.loads(text)
    if isinstance(data, dict):
        data = data.get("data", [data])
    if not isinstance(data, list) or not all(isinstance(row, dict) for row in data):
        raise ValueError("JSON input must be an object, a list of objects, or an object containing a data list.")
    return normalize_rows(data)


def load_text(text: str, *, fmt: str = "auto") -> list[dict[str, Any]]:
    if fmt == "csv":
        return load_csv(text)
    if fmt == "json":
        return load_json(text)
    stripped = text.lstrip()
    if stripped.startswith("[") or stripped.startswith("{"):
        return load_json(text)
    return load_csv(text)


def validate_rows(rows: Iterable[dict[str, Any]]) -> dict[str, Any]:
    rows = list(rows)
    warnings: list[str] = []
    if not rows:
        warnings.append("No rows were imported.")
        return {"valid": False, "row_count": 0, "warnings": warnings}
    if not any("spend" in row for row in rows):
        warnings.append("No spend field was detected; CPA/ROAS/budget analysis may be unavailable.")
    if not any("impressions" in row for row in rows):
        warnings.append("No impressions field was detected; CPM/CTR may be unavailable.")
    if not any("conversions" in row for row in rows):
        warnings.append("No conversions field was detected; CPA/conversion analysis may be unavailable.")
    return {"valid": True, "row_count": len(rows), "warnings": warnings}
