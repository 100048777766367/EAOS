"""Gateway contract schemas observed by AIDE."""

from typing import Any, Literal

from pydantic import BaseModel, ConfigDict, Field

ContractState = Literal["available", "unavailable", "degraded", "missing"]


class GatewayContract(BaseModel):
    """A contract AIDE can consume from the Enterprise Gateway."""

    model_config = ConfigDict(frozen=True)

    name: str
    method: str
    path: str
    owner: str = "apps/api"
    state: ContractState = "available"
    purpose: str


class GatewayResult(BaseModel):
    """Observed response from a Gateway request."""

    model_config = ConfigDict(frozen=True)

    contract: str
    target: str
    status: ContractState
    detail: str
    payload: dict[str, Any] = Field(default_factory=dict)
