from __future__ import annotations

from enum import StrEnum

from pydantic import BaseModel, ConfigDict, Field

"""11 Federated Governance Boards Domain Models (ADR-GOV-001)."""


class BoardID(StrEnum):
    """11 Federated Governance Boards for EAOS Enterprise Lifecycle."""

    BUSINESS = "business_board"
    ARCHITECTURE = "architecture_board"
    EXPERIENCE = "experience_board"
    ENGINEERING = "engineering_board"
    PLATFORM = "platform_board"
    SECURITY = "security_board"
    QUALITY = "quality_board"
    OPERATIONS = "operations_board"
    AI = "ai_board"
    KNOWLEDGE = "knowledge_board"
    GOVERNANCE = "governance_board"


class BoardCharterDTO(BaseModel):
    """Charter specification for a Federated Governance Board."""

    model_config = ConfigDict(frozen=True)

    board_id: BoardID = Field(..., description="Unique board ID")
    title: str = Field(..., description="Canonical board title")
    primary_responsibility: str = Field(..., description="Focus area")
    key_outcomes: str = Field(..., description="Measurable outcomes")
    roles_covered: list[str] = Field(default_factory=list)


class BoardAuditReportDTO(BaseModel):
    """Audit report for all 11 Federated Governance Boards."""

    model_config = ConfigDict(frozen=True)

    total_boards: int = Field(default=11)
    passed_boards: int = Field(default=11)
    charters: list[BoardCharterDTO] = Field(default_factory=list)
    constitutional_compliance: bool = Field(default=True)
