from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field

"""Domain Entities Catalog (DDD Pattern)."""


class EntityElementDTO(BaseModel):
    """Value object representing a DDD Entity in Enterprise Catalog."""

    model_config = ConfigDict(frozen=True)

    entity_id: str = Field(..., description="Entity ID")
    name: str = Field(..., description="Entity name")
    attributes_count: int = Field(default=0)


class EntityCatalogRegistry:
    """Registry cataloging domain entities."""

    def get_default_entities(self) -> list[EntityElementDTO]:
        """Return standard domain entities."""
        return [
            EntityElementDTO(entity_id="ent-user", name="User", attributes_count=5),
            EntityElementDTO(entity_id="ent-adr", name="ADRRecord", attributes_count=7),
        ]
