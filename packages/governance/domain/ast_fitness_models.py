from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field

"""AST Fitness Functions Domain Models (Phase 2)."""


class ASTFitnessViolation(BaseModel):
    """Value object representing an architecture AST violation."""

    model_config = ConfigDict(frozen=True)

    file_path: str = Field(..., description="File path with violation")
    line_number: int = Field(..., description="Line number")
    rule_id: str = Field(..., description="Rule ID e.g. R01")
    message: str = Field(..., description="Violation message")


class ASTFitnessReport(BaseModel):
    """Aggregate report for AST architecture inspection."""

    model_config = ConfigDict(frozen=True)

    score: float = Field(default=100.0, description="Fitness score 0-100")
    total_files_scanned: int = Field(default=0)
    violations: list[ASTFitnessViolation] = Field(default_factory=list)
    passed: bool = Field(default=True)
