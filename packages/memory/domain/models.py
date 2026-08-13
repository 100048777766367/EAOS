from datetime import UTC, datetime

from pydantic import BaseModel, ConfigDict, Field

"""Memory Domain Models."""


class MemoryItem(BaseModel):
    """Representing a generic memory item."""

    memory_id: str
    content: str
    author: str = "system"
    created_at: datetime = Field(default_factory=lambda: datetime.now(UTC))

    model_config = ConfigDict(frozen=True)
