"""AIDE Gateway HTTP client adapters."""

import json
from asyncio import to_thread
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

from apps.aide.app.schemas.gateway import GatewayResult
from apps.aide.app.settings import AideSettings


def _request_json(
    method: str,
    target: str,
    payload: dict[str, Any] | None,
) -> tuple[int, dict[str, Any]]:
    data = None if payload is None else json.dumps(payload).encode("utf-8")
    request = Request(
        target,
        data=data,
        headers={"Content-Type": "application/json"},
        method=method,
    )
    with urlopen(request, timeout=2.0) as response:
        body = response.read().decode("utf-8")
        status_code = getattr(response, "status", 0)
    parsed = json.loads(body) if body else {}
    return status_code, parsed if isinstance(parsed, dict) else {"data": parsed}


async def request_gateway_json(
    settings: AideSettings,
    contract: str,
    method: str,
    path: str,
    payload: dict[str, Any] | None = None,
) -> GatewayResult:
    """Call an existing Gateway endpoint and preserve failure state."""

    target = f"{str(settings.api_base_url).rstrip('/')}{path}"
    try:
        status_code, response = await to_thread(
            _request_json,
            method,
            target,
            payload,
        )
    except HTTPError as exc:
        return GatewayResult(
            contract=contract,
            target=target,
            status="degraded",
            detail=f"HTTP {exc.code}",
        )
    except (OSError, URLError, TimeoutError) as exc:
        return GatewayResult(
            contract=contract,
            target=target,
            status="unavailable",
            detail=str(exc),
        )

    if 200 <= status_code < 300:
        return GatewayResult(
            contract=contract,
            target=target,
            status="available",
            detail=f"HTTP {status_code}",
            payload=response,
        )
    return GatewayResult(
        contract=contract,
        target=target,
        status="degraded",
        detail=f"HTTP {status_code}",
        payload=response,
    )
