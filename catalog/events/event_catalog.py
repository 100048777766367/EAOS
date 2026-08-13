from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field

"""Domain Events Catalog (EDA Pattern)."""


class EventElementDTO(BaseModel):
    """Value object representing a Domain Event in Enterprise Catalog."""

    model_config = ConfigDict(frozen=True)

    event_id: str = Field(..., description="Event ID")
    name: str = Field(..., description="Event name e.g. PatchApplied")
    topic: str = Field(default="events.domain")


class EventCatalogRegistry:
    """Registry cataloging domain events."""

    def get_default_events(self) -> list[EventElementDTO]:
        """Return standard domain events."""
        return [
            EventElementDTO(
                event_id="evt-patch-applied",
                name="PatchAppliedEvent",
                topic="events.system",
            ),
        ]
