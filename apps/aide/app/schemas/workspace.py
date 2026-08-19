"""AIDE workspace schemas."""

from pydantic import BaseModel, ConfigDict


class CapabilityLink(BaseModel):
    """Gateway or platform capability consumed by AIDE."""

    model_config = ConfigDict(frozen=True)

    name: str
    owner: str
    transport: str
    endpoint: str


class AideWorkspaceState(BaseModel):
    """Initial browser state for the AIDE workspace shell."""

    model_config = ConfigDict(frozen=True)

    app_name: str
    api_base_url: str
    api_ws_url: str
    web_url: str
    default_workspace: str
    capabilities: list[CapabilityLink]
