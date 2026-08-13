from datetime import UTC, datetime
from enum import StrEnum

from pydantic import BaseModel, ConfigDict, Field

"""Process Architecture Frameworks & Methodologies for EAOS."""


class ProcessFrameworkType(StrEnum):
    """Enumeration of 10 Process Architecture Frameworks."""

    APQC_PCF = "APQC_PCF"
    SCOR = "SCOR"
    DCOR = "DCOR"
    CCOR = "CCOR"
    BPM_CBOK = "BPM_CBOK"
    BPMN = "BPMN"
    SIPOC = "SIPOC"
    LEAN = "LEAN"
    SIX_SIGMA = "SIX_SIGMA"
    LEAN_SIX_SIGMA = "LEAN_SIX_SIGMA"


class ProcessMappingElement(BaseModel):
    """Value object mapping a process element to an EAOS workflow."""

    model_config = ConfigDict(frozen=True)

    framework_type: ProcessFrameworkType
    process_name: str
    target_workflow_id: str
    sipoc_inputs: tuple[str, ...] = ()
    sipoc_outputs: tuple[str, ...] = ()


class ProcessFrameworkProfile(BaseModel):
    """Entity representing an ingested Process Architecture Model."""

    model_config = ConfigDict(frozen=True)

    profile_id: str = Field(..., description="Unique Profile UUID")
    framework_type: ProcessFrameworkType
    name: str
    mappings: tuple[ProcessMappingElement, ...] = ()
    created_at: datetime = Field(default_factory=lambda: datetime.now(UTC))
