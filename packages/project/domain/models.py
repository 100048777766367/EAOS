from datetime import UTC, datetime

from pydantic import BaseModel, ConfigDict, Field

"""Project Management Capability Domain Models for EAOS."""


class ProjectTask(BaseModel):
    """Value object representing an enterprise project task."""

    model_config = ConfigDict(frozen=True)

    task_id: str = Field(..., description="Unique Task ID")
    project_name: str = Field(..., description="Project name")
    title: str = Field(..., description="Task title")
    assignee_id: str = Field(default="AI_AGENT_01")
    status: str = Field(default="IN_PROGRESS")
    created_at: datetime = Field(default_factory=lambda: datetime.now(UTC))
