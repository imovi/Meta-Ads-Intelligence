"""High-level Meta Ads operations built on top of meta_api_client.

These helpers keep API object paths and common fields in one place. They do not
make authorization decisions; the Skill/action_guard must do that first.
"""

from __future__ import annotations

from typing import Any, Dict, Iterable, Optional

from meta_api_client import get_insights, get_object, paginate, request, write_object


CAMPAIGN_FIELDS = [
    "id", "name", "status", "effective_status", "objective", "daily_budget",
    "lifetime_budget", "start_time", "stop_time", "created_time", "updated_time",
]

ADSET_FIELDS = [
    "id", "name", "status", "effective_status", "campaign_id", "daily_budget",
    "lifetime_budget", "billing_event", "optimization_goal", "bid_strategy",
    "start_time", "end_time",
]

AD_FIELDS = [
    "id", "name", "status", "effective_status", "adset_id", "campaign_id",
    "creative", "created_time", "updated_time",
]

INSIGHT_FIELDS = [
    "date_start", "date_stop", "campaign_id", "campaign_name", "adset_id",
    "adset_name", "ad_id", "ad_name", "impressions", "reach", "frequency",
    "clicks", "outbound_clicks", "spend", "cpm", "cpc", "ctr", "actions",
    "action_values", "cost_per_action_type",
]


def account(account_id: str, fields: Optional[Iterable[str]] = None) -> Dict[str, Any]:
    return get_object(account_id, fields or ["id", "name", "account_status", "currency", "timezone_name"])


def campaign(campaign_id: str) -> Dict[str, Any]:
    return get_object(campaign_id, CAMPAIGN_FIELDS)


def adset(adset_id: str) -> Dict[str, Any]:
    return get_object(adset_id, ADSET_FIELDS)


def ad(ad_id: str) -> Dict[str, Any]:
    return get_object(ad_id, AD_FIELDS)


def list_children(parent_id: str, child_type: str, fields: Iterable[str], *, params: Optional[Dict[str, Any]] = None) -> list[Dict[str, Any]]:
    query = dict(params or {})
    query["fields"] = ",".join(fields)
    first = request(f"{parent_id}/{child_type}", params=query)
    return paginate(first)


def campaigns(account_id: str, *, params: Optional[Dict[str, Any]] = None) -> list[Dict[str, Any]]:
    return list_children(account_id, "campaigns", CAMPAIGN_FIELDS, params=params)


def adsets(campaign_id: str, *, params: Optional[Dict[str, Any]] = None) -> list[Dict[str, Any]]:
    return list_children(campaign_id, "adsets", ADSET_FIELDS, params=params)


def ads(adset_id: str, *, params: Optional[Dict[str, Any]] = None) -> list[Dict[str, Any]]:
    return list_children(adset_id, "ads", AD_FIELDS, params=params)


def insights(object_id: str, *, date_start: str, date_stop: str, fields: Optional[Iterable[str]] = None, level: Optional[str] = None, breakdowns: Optional[Iterable[str]] = None, **extra: Any) -> list[Dict[str, Any]]:
    params: Dict[str, Any] = {"time_range": f'{{"since":"{date_start}","until":"{date_stop}"}}'}
    if level:
        params["level"] = level
    if breakdowns:
        params["breakdowns"] = ",".join(breakdowns)
    params.update(extra)
    first = get_insights(object_id, fields=fields or INSIGHT_FIELDS, **params)
    return paginate(first)


def pause(object_id: str) -> Dict[str, Any]:
    return write_object(object_id, data={"status": "PAUSED"})


def resume(object_id: str) -> Dict[str, Any]:
    return write_object(object_id, data={"status": "ACTIVE"})


def update(object_id: str, data: Dict[str, Any]) -> Dict[str, Any]:
    return write_object(object_id, data=data)


def create(parent_id: str, object_type: str, data: Dict[str, Any]) -> Dict[str, Any]:
    return write_object(f"{parent_id}/{object_type}", data=data)
