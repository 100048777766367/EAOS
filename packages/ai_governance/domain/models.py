from datetime import UTC, datetime
from enum import StrEnum

from pydantic import BaseModel, ConfigDict, Field

"""AI Architecture & AI Governance Frameworks Domain Model for EAOS."""


class AIGovernanceFrameworkType(StrEnum):
    """Enumeration of 9 AI Architecture & Governance Standards."""

    NIST_AI_RMF = "NIST_AI_RMF"
    ISO_42001 = "ISO_42001"
    ISO_23894 = "ISO_23894"
    MS_RESPONSIBLE_AI = "MS_RESPONSIBLE_AI"
    GOOGLE_SAIF = "GOOGLE_SAIF"
    OWASP_LLM_TOP10 = "OWASP_LLM_TOP10"
    MLOPS = "MLOPS"
    LLMOPS = "LLMOPS"
    AGENTOPS = "AGENTOPS"


class AIGovernanceProfile(BaseModel):
    """Value object representing an ingested AI Governance Profile."""

    model_config = ConfigDict(frozen=True)

    profile_id: str = Field(..., description="Unique Profile ID")
    framework_type: AIGovernanceFrameworkType
    name: str
    is_active: bool = True
    created_at: datetime = Field(default_factory=lambda: datetime.now(UTC))
