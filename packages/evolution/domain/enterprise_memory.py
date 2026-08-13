from __future__ import annotations

from datetime import UTC, datetime
from enum import StrEnum

from pydantic import BaseModel, ConfigDict, Field

"""Enterprise Memory Domain Models (v4.x Autonomous Learning)."""


class MemoryCategory(StrEnum):
    """10-Category Enterprise Memory classification."""

    BUSINESS = "BUSINESS"
    ARCHITECTURE = "ARCHITECTURE"
    ENGINEERING = "ENGINEERING"
    SECURITY = "SECURITY"
    AI_INTERACTION = "AI_INTERACTION"
    INCIDENT = "INCIDENT"
    CUSTOMER = "CUSTOMER"
    GOVERNANCE = "GOVERNANCE"
    COMPLIANCE = "COMPLIANCE"
    OPERATIONAL = "OPERATIONAL"


class EnterpriseMemoryRecord(BaseModel):
    """Rich aggregate memory record representing organizational intelligence."""

    model_config = ConfigDict(frozen=True)

    memory_id: str = Field(..., description="Unique memory ID")
    category: MemoryCategory = Field(default=MemoryCategory.INCIDENT)
    capability_id: str = Field(default="cap-core")
    architecture_component: str = Field(default="kernel")
    evidence_summary: str = Field(..., description="Observed evidence")
    root_cause: str = Field(default="", description="Root cause analysis")
    corrective_action: str = Field(default="", description="Immediate fix")
    preventive_action: str = Field(default="", description="Long-term rule")
    lessons: list[str] = Field(default_factory=list)
    generated_rules: list[str] = Field(default_factory=list)
    generated_adrs: list[str] = Field(default_factory=list)
    confidence_score: float = Field(default=1.0)
    impact_score: float = Field(default=1.0)
    recurrence_probability: float = Field(default=0.0)
    linked_knowledge_nodes: list[str] = Field(default_factory=list)
    timestamp: datetime = Field(default_factory=lambda: datetime.now(UTC))
