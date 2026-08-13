from typing import ClassVar

from pydantic import BaseModel, ConfigDict

"""Ecosystem Adapter managing platform infrastructure registry."""


class EcosystemMemberDTO(BaseModel):
    """Value object representing an ecosystem federation member."""

    model_config = ConfigDict(frozen=True)

    member_id: str
    role: str
    status: str = "ACTIVE"


class ToolMappingDTO(BaseModel):
    """Value object representing external tool mapping for a capability."""

    model_config = ConfigDict(frozen=True)

    external_tool_name: str = "github_and_opa"


class EcosystemIntegrationEngine:
    """Adapter managing active ecosystem members, roles, and tools."""

    DEFAULT_MEMBERS: ClassVar[tuple[EcosystemMemberDTO, ...]] = (
        EcosystemMemberDTO(member_id="MEMBER-01", role="LEADER"),
        EcosystemMemberDTO(member_id="MEMBER-02", role="FOLLOWER"),
    )

    def list_members(self) -> list[EcosystemMemberDTO]:
        """Returns list of active ecosystem members."""
        return list(self.DEFAULT_MEMBERS)

    def resolve_tool_for_capability(self, capability_name: str) -> ToolMappingDTO:
        """Resolves tool mapping for target capability."""
        return ToolMappingDTO(external_tool_name="github_and_opa")


# Aliases for legacy integration engine compatibility
InMemoryEcosystemAdapter = EcosystemIntegrationEngine
