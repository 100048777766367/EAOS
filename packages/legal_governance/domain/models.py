from datetime import UTC, datetime
from enum import StrEnum

from pydantic import BaseModel, ConfigDict, Field

"""Legal Governance & Judicial System Domain Model for EAOS."""


class JudicialRole(StrEnum):
    """Roles within the EAOS Architectural Court System."""

    JUDGE = "JUDGE"
    PROSECUTOR = "PROSECUTOR"
    DEFENDANT = "DEFENDANT"
    DEFENSE_COUNSEL = "DEFENDANT_ADVOCATE"
    JURY = "JURY"


class LegalVerdictDTO(BaseModel):
    """Value object representing a judicial court verdict."""

    model_config = ConfigDict(frozen=True)

    trial_id: str
    target_artifact: str
    verdict: str
    sanction_action: str
    evidence_hash: str
    timestamp: datetime = Field(default_factory=lambda: datetime.now(UTC))
