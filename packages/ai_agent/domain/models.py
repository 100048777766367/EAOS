from datetime import UTC, datetime

from pydantic import BaseModel, ConfigDict, Field

"""AI Agent Management Domain Models for EAOS."""


class AIAgentProfile(BaseModel):
    """Value object representing an autonomous AI agent definition."""

    model_config = ConfigDict(frozen=True)

    agent_id: str = Field(..., description="Unique Agent ID")
    role: str = Field(..., description="Agent role title")
    model_name: str = Field(default="claude-3.5-sonnet")
    temperature: float = Field(default=0.2)
    status: str = Field(default="READY")
    created_at: datetime = Field(default_factory=lambda: datetime.now(UTC))
