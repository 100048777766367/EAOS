from __future__ import annotations

from typing import Any

from pydantic import BaseModel, ConfigDict, Field

"""Enterprise Operations Architecture (EOA) Domain Models."""


class OpsRuleDTO(BaseModel):
    """Value object representing an Operations Constitution rule."""

    model_config = ConfigDict(frozen=True)

    rule_id: str = Field(..., description="Rule ID e.g. OPS-001")
    name: str = Field(..., description="Rule name")
    statement: str = Field(..., description="Immutable rule statement")
    severity: str = Field(default="CRITICAL")


class OpsCapabilityDTO(BaseModel):
    """Aggregate representing an operational capability."""

    model_config = ConfigDict(frozen=True)

    capability_id: str = Field(..., description="Capability ID e.g. OPS-CAP-001")
    name: str = Field(..., description="Capability name e.g. Backup")
    purpose: str = Field(..., description="Business purpose")
    owner: str = Field(default="Platform Team")
    slo_target: str = Field(default="99.99%")
    dependencies: list[str] = Field(default_factory=list)


class OpsExecutableRunbookDTO(BaseModel):
    """Declarative executable runbook in EOA Layer 7."""

    model_config = ConfigDict(frozen=True)

    runbook_id: str = Field(..., description="Runbook ID")
    capability_id: str = Field(..., description="Target capability ID")
    steps: list[dict[str, Any]] = Field(default_factory=list)
    automated: bool = Field(default=True)
