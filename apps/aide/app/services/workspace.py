"""Workspace composition service for AIDE."""

from apps.aide.app.adapters.gateway import build_gateway_contracts
from apps.aide.app.schemas.workspace import AideWorkspaceState
from apps.aide.app.settings import AideSettings


def build_workspace_state(settings: AideSettings) -> AideWorkspaceState:
    """Build the immutable state injected into the browser workspace."""

    return AideWorkspaceState(
        app_name=settings.title,
        api_base_url=str(settings.api_base_url).rstrip("/"),
        api_ws_url=settings.api_ws_url,
        web_url=str(settings.web_url).rstrip("/"),
        default_workspace="EAOS",
        capabilities=build_gateway_contracts(settings),
    )
