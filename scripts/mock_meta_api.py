"""Deterministic mock data for local Skill tests.

This module never calls Meta. It lets evals exercise analysis and action routing
without credentials or spending money.
"""

from __future__ import annotations

from copy import deepcopy


DATA = {
    "account": {"id": "act_mock_001", "name": "Demo Store", "currency": "USD", "account_status": 1},
    "campaigns": [
        {"id": "camp_001", "name": "Prospecting - Sales", "status": "ACTIVE", "objective": "OUTCOME_SALES", "daily_budget": 100},
        {"id": "camp_002", "name": "Retargeting - Sales", "status": "ACTIVE", "objective": "OUTCOME_SALES", "daily_budget": 50},
    ],
    "adsets": [
        {"id": "set_001", "campaign_id": "camp_001", "name": "Broad", "status": "ACTIVE", "daily_budget": 100},
        {"id": "set_002", "campaign_id": "camp_002", "name": "Website Visitors", "status": "ACTIVE", "daily_budget": 50},
    ],
    "ads": [
        {"id": "ad_001", "adset_id": "set_001", "campaign_id": "camp_001", "name": "UGC Hook A", "status": "ACTIVE"},
        {"id": "ad_002", "adset_id": "set_001", "campaign_id": "camp_001", "name": "Product Demo B", "status": "ACTIVE"},
        {"id": "ad_003", "adset_id": "set_002", "campaign_id": "camp_002", "name": "Offer C", "status": "ACTIVE"},
    ],
    "insights": [
        {"ad_id": "ad_001", "ad_name": "UGC Hook A", "spend": 120, "impressions": 18000, "reach": 12000, "clicks": 540, "conversions": 12, "revenue": 720},
        {"ad_id": "ad_002", "ad_name": "Product Demo B", "spend": 120, "impressions": 22000, "reach": 14000, "clicks": 396, "conversions": 5, "revenue": 300},
        {"ad_id": "ad_003", "ad_name": "Offer C", "spend": 80, "impressions": 9000, "reach": 5000, "clicks": 315, "conversions": 10, "revenue": 650},
    ],
}


def snapshot() -> dict:
    return deepcopy(DATA)


def find(object_id: str) -> dict | None:
    for group in ("campaigns", "adsets", "ads"):
        for item in DATA[group]:
            if item["id"] == object_id:
                return deepcopy(item)
    if object_id == DATA["account"]["id"]:
        return deepcopy(DATA["account"])
    return None


def set_status(object_id: str, status: str) -> dict:
    for group in ("campaigns", "adsets", "ads"):
        for item in DATA[group]:
            if item["id"] == object_id:
                item["status"] = status
                return deepcopy(item)
    raise KeyError(object_id)


def set_daily_budget(object_id: str, value: float) -> dict:
    for group in ("campaigns", "adsets"):
        for item in DATA[group]:
            if item["id"] == object_id:
                item["daily_budget"] = value
                return deepcopy(item)
    raise KeyError(object_id)
