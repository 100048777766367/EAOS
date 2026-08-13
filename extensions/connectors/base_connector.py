from __future__ import annotations

from typing import Protocol, runtime_checkable

from pydantic import BaseModel, ConfigDict, Field

"""Base Connector Protocol for Third-Party Integrations."""


class ConnectorStatusDTO(BaseModel):
    """Value object representing connector operational status."""

    model_config = ConfigDict(frozen=True)

    connector_id: str = Field(..., description="Unique connector ID")
    name: str = Field(..., description="Connector canonical name")
    is_connected: bool = Field(default=True)
    protocol_type: str = Field(default="REST")


@runtime_checkable
class BaseEcosystemConnector(Protocol):
    """Protocol defining the contract for external ecosystem connectors."""

    connector_id: str
    name: str

    async def connect(self) -> bool: ...

    async def check_health(self) -> ConnectorStatusDTO: ...
