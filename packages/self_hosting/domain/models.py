from datetime import UTC, datetime

from pydantic import BaseModel, ConfigDict, Field

"""Self-Hosting & Dogfooding Domain Model for EAOS Platform."""


class EAOSRepositoryHealth(BaseModel):
    """Value object representing EAOS self-audit metrics."""

    model_config = ConfigDict(frozen=True)

    system_id: str = Field(default="EAOS-SELF-HOSTED")
    total_source_files: int
    active_capabilities_count: int
    architecture_score: float = Field(default=100.0)
    drift_index: float = Field(default=0.0)
    timestamp: datetime = Field(default_factory=lambda: datetime.now(UTC))


class DogfoodingTaskStatus(BaseModel):
    """Entity representing an EAOS self-managed task item."""

    model_config = ConfigDict(frozen=True)

    task_code: str
    title: str
    capability_bound: str
    is_completed: bool = False
