from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field

"""CQRS Commands Catalog (CQRS Pattern)."""


class CommandElementDTO(BaseModel):
    """Value object representing a CQRS Command in Enterprise Catalog."""

    model_config = ConfigDict(frozen=True)

    command_id: str = Field(..., description="Command ID")
    name: str = Field(..., description="Command name e.g. CreateUser")
    target_aggregate: str = Field(..., description="Target Aggregate")


class CommandCatalogRegistry:
    """Registry cataloging CQRS commands."""

    def get_default_commands(self) -> list[CommandElementDTO]:
        """Return standard CQRS commands."""
        return [
            CommandElementDTO(
                command_id="cmd-create-user",
                name="CreateUserCommand",
                target_aggregate="Customer Aggregate",
            ),
            CommandElementDTO(
                command_id="cmd-apply-patch",
                name="ApplyPatchCommand",
                target_aggregate="Policy Aggregate",
            ),
        ]
