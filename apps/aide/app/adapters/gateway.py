"""Client-side contract map for the EAOS Engineering Gateway."""

from apps.aide.app.schemas.workspace import CapabilityLink
from apps.aide.app.settings import AideSettings


def build_gateway_contracts(settings: AideSettings) -> list[CapabilityLink]:
    """Describe API capabilities AIDE consumes without owning them."""

    base = str(settings.api_base_url).rstrip("/")
    return [
        CapabilityLink(
            name="health",
            owner="apps/api",
            transport="HTTP",
            endpoint=f"{base}/health",
        ),
        CapabilityLink(
            name="agents",
            owner="apps/api",
            transport="HTTP",
            endpoint=f"{base}/v1/agents/execute",
        ),
        CapabilityLink(
            name="chat-stream",
            owner="apps/api",
            transport="WebSocket",
            endpoint=settings.api_ws_url,
        ),
        CapabilityLink(
            name="runtime-capabilities",
            owner="apps/api",
            transport="HTTP",
            endpoint=f"{base}/v1/capabilities",
        ),
        CapabilityLink(
            name="governance",
            owner="apps/api",
            transport="HTTP",
            endpoint=f"{base}/governance/opa/evaluate",
        ),
        CapabilityLink(
            name="knowledge",
            owner="apps/api",
            transport="HTTP",
            endpoint=f"{base}/v1/knowledge/topology",
        ),
        CapabilityLink(
            name="telemetry",
            owner="apps/api",
            transport="HTTP",
            endpoint=f"{base}/telemetry/ingest",
        ),
    ]
