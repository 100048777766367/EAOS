"""Data Transfer Objects for Capability Mapping application layer."""

from pathlib import Path

from pydantic import BaseModel, Field

from packages.capability_mapping.domain.models import (
    CapabilityMaturityLevel,
    RealizationType,
)


class BindingDTO(BaseModel):
    target_ref: str = Field(..., description="Package or component path")
    realization_type: RealizationType
    description: str


class RegisterCapabilityMappingCommand(BaseModel):
    capability_id: str
    capability_name: str
    domain_group: str
    maturity_level: CapabilityMaturityLevel = CapabilityMaturityLevel.DEFINED
    bindings: list[BindingDTO] = Field(default_factory=list)


class AnalyzeCapabilityGapsQuery(BaseModel):
    workspace_root: Path


class CapabilityGapReport(BaseModel):
    capability_id: str
    capability_name: str
    coverage_percentage: float
    broken_bindings: list[str]
    status: str  # "HEALTHY" | "DEGRADED" | "UNREALIZED"
