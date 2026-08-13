from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field

"""Ecosystem Enterprise Node Registry Engine."""


class EcosystemMemberDTO(BaseModel):
    """Value object representing an enterprise ecosystem member."""

    model_config = ConfigDict(frozen=True)

    enterprise_id: str = Field(..., description="Unique enterprise ID")
    name: str = Field(..., description="Enterprise name")
    region: str = Field(default="us-east-1")
    is_active: bool = Field(default=True)


class EcosystemRegistryEngine:
    """Registry tracking member enterprises in federated network."""

    def __init__(self) -> None:
        self._members: dict[str, EcosystemMemberDTO] = {}
        self._register_default_members()

    def _register_default_members(self) -> None:
        node1 = EcosystemMemberDTO(
            enterprise_id="ent-node-01",
            name="Core Enterprise Node 1",
            region="local-prod",
        )
        self._members[node1.enterprise_id] = node1

    def list_members(self) -> list[EcosystemMemberDTO]:
        """Return list of active ecosystem member nodes."""
        return list(self._members.values())
