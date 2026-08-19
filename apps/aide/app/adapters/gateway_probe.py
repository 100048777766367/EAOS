"""Small AIDE adapter for observing Gateway availability."""

from asyncio import to_thread
from urllib.error import URLError
from urllib.request import urlopen

from apps.aide.app.schemas.integration import GatewayProbe
from apps.aide.app.settings import AideSettings


def _probe_url(target: str) -> tuple[str, str]:
    with urlopen(target, timeout=1.5) as response:
        status_code = getattr(response, "status", 0)
    if 200 <= status_code < 300:
        return "observed", "HTTP OK"
    return "degraded", f"HTTP {status_code}"


async def probe_gateway(settings: AideSettings) -> GatewayProbe:
    """Probe the API Gateway without implementing Gateway behavior."""

    target = f"{str(settings.api_base_url).rstrip('/')}/health"
    try:
        status, detail = await to_thread(_probe_url, target)
        return GatewayProbe(target=target, status=status, detail=detail)
    except (OSError, URLError) as exc:
        return GatewayProbe(target=target, status="unavailable", detail=str(exc))
