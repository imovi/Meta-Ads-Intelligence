"""Small dependency-free Meta Marketing API adapter.

This module deliberately does not contain credentials or a fixed Graph API version.
The caller supplies the API base URL and access token at runtime. It supports read
requests and explicit write requests while leaving confirmation/policy decisions
to the skill layer.
"""

from __future__ import annotations

import os
from typing import Any, Dict, Iterable, Optional
from urllib.parse import urlencode
from urllib.request import Request, urlopen
from urllib.error import HTTPError, URLError
import json


class MetaAPIError(RuntimeError):
    """Raised when the Meta API request fails."""


def _env(name: str) -> Optional[str]:
    value = os.getenv(name)
    return value.strip() if value else None


def _base_url() -> str:
    return (_env("META_GRAPH_API_BASE_URL") or "https://graph.facebook.com").rstrip("/")


def _token(access_token: Optional[str]) -> str:
    token = access_token or _env("META_ACCESS_TOKEN")
    if not token:
        raise MetaAPIError("Missing META_ACCESS_TOKEN. Provide it through the environment or a secure secret store.")
    return token


def request(
    path: str,
    *,
    method: str = "GET",
    params: Optional[Dict[str, Any]] = None,
    access_token: Optional[str] = None,
    timeout: int = 30,
) -> Dict[str, Any]:
    """Make a JSON request to Meta's Graph API.

    The API version is intentionally part of `path` or the configured base URL;
    this adapter does not guess a version that may become stale.
    """
    clean_path = "/" + path.lstrip("/")
    query = dict(params or {})
    query["access_token"] = _token(access_token)
    url = f"{_base_url()}{clean_path}"

    if method.upper() == "GET":
        url = f"{url}?{urlencode(query, doseq=True)}"
        data = None
    else:
        data = urlencode(query, doseq=True).encode("utf-8")

    req = Request(url, data=data, method=method.upper(), headers={"Accept": "application/json"})

    try:
        with urlopen(req, timeout=timeout) as response:
            payload = json.loads(response.read().decode("utf-8"))
    except HTTPError as exc:
        raw = exc.read().decode("utf-8", errors="replace")
        try:
            payload = json.loads(raw)
        except json.JSONDecodeError:
            payload = {"error": {"message": raw or str(exc)}}
        raise MetaAPIError(json.dumps(payload, ensure_ascii=False)) from exc
    except URLError as exc:
        raise MetaAPIError(f"Meta API connection failed: {exc.reason}") from exc

    if isinstance(payload, dict) and payload.get("error"):
        raise MetaAPIError(json.dumps(payload["error"], ensure_ascii=False))
    return payload


def get_object(object_id: str, fields: Optional[Iterable[str]] = None, **kwargs: Any) -> Dict[str, Any]:
    params: Dict[str, Any] = {}
    if fields:
        params["fields"] = ",".join(fields)
    return request(object_id, params=params, **kwargs)


def get_insights(object_id: str, *, fields: Iterable[str], **params: Any) -> Dict[str, Any]:
    query = dict(params)
    query["fields"] = ",".join(fields)
    return request(f"{object_id}/insights", params=query)


def write_object(object_id: str, *, data: Dict[str, Any], method: str = "POST", **kwargs: Any) -> Dict[str, Any]:
    """Perform an explicit write. Caller must enforce confirmation before calling."""
    return request(object_id, method=method, params=data, **kwargs)


def paginate(first_page: Dict[str, Any], *, max_pages: int = 100) -> list[Dict[str, Any]]:
    """Collect Graph API pages without exposing access tokens in returned data."""
    rows: list[Dict[str, Any]] = []
    page = first_page
    for _ in range(max_pages):
        rows.extend(page.get("data", []) or [])
        next_url = ((page.get("paging") or {}).get("next"))
        if not next_url:
            break
        req = Request(next_url, headers={"Accept": "application/json"})
        try:
            with urlopen(req, timeout=30) as response:
                page = json.loads(response.read().decode("utf-8"))
        except Exception as exc:
            raise MetaAPIError(f"Pagination request failed: {exc}") from exc
    return rows


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Minimal Meta Graph API reader")
    parser.add_argument("object_id")
    parser.add_argument("--fields", nargs="*", default=[])
    args = parser.parse_args()

    print(json.dumps(get_object(args.object_id, args.fields), indent=2, ensure_ascii=False))
