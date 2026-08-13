from __future__ import annotations

from enum import StrEnum

from pydantic import BaseModel, ConfigDict, Field

"""Data Transfer Objects for EAOS Doctor (SOLID OCP)."""


class SeverityLevel(StrEnum):
    """Severity level enum for diagnostic checks."""

    PASS = "PASS"
    INFO = "INFO"
    WARN = "WARN"
    ERROR = "ERROR"
    CRITICAL = "CRITICAL"


class DiagnosticCheckDTO(BaseModel):
    """Value object representing an individual diagnostic check."""

    model_config = ConfigDict(frozen=True)

    checker_id: str = Field(..., description="Checker ID e.g. validator")
    category: str = Field(..., description="Category e.g. Runtime")
    name: str = Field(..., description="Check name e.g. Python")
    severity: SeverityLevel = Field(default=SeverityLevel.PASS)
    status: str = Field(..., description="PASS, FAIL, WARN")
    message: str = Field(..., description="Detail or version string")


class DiagnosticReportDTO(BaseModel):
    """Aggregate report DTO for enterprise system diagnostic."""

    model_config = ConfigDict(frozen=True)

    status: str = Field(default="READY")
    overall_health_score: int = Field(default=100)
    total_checks: int = Field(default=0)
    passed_checks: int = Field(default=0)
    failed_checks: int = Field(default=0)
    checks: list[DiagnosticCheckDTO] = Field(default_factory=list)
    categories: list[str] = Field(default_factory=list)
    ast_compliant: bool = Field(default=True)
