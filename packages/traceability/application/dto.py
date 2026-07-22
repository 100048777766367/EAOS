"""Data Transfer Objects for Traceability application layer."""

from pathlib import Path

from packages.traceability.domain.models import CausalNodeType
from pydantic import BaseModel, Field


class CausalNodeDTO(BaseModel):
    node_id: str
    node_type: CausalNodeType
    title: str
    description: str
    evidence_payload: dict[str, str | float | int | bool] = Field(
        default_factory=dict
    )


class RecordTraceCommand(BaseModel):
    trace_id: str
    file_path: Path
    start_line: int
    end_line: int
    commit_hash: str | None = None
    nodes: list[CausalNodeDTO]


class ExplainCodeChangeQuery(BaseModel):
    file_path: Path
    line_number: int


class CodeChangeExplanationResponse(BaseModel):
    trace_id: str | None
    file_path: str
    line_number: int
    explanation: str
    found: bool
