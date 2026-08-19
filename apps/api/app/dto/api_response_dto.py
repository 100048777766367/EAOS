"""API Response and Request DTOs."""

from typing import Any

from pydantic import BaseModel, ConfigDict, Field


class HealthResponse(BaseModel):
    """API Gateway Health DTO."""

    status: str
    version: str
    governance: str
    doctor_score: int = 100


class APIStandardResponseDTO(BaseModel):
    """Standard API envelope response DTO."""

    model_config = ConfigDict(frozen=True)

    status: str = "SUCCESS"
    message: str = ""
    data: dict[str, Any] = Field(default_factory=dict)


class RegoEvalRequest(BaseModel):
    """Rego evaluation request DTO."""

    model_config = ConfigDict(frozen=True)
    rego_script: str
    payload: dict[str, Any]


class RaftProposeRequest(BaseModel):
    """Raft consensus proposal DTO."""

    model_config = ConfigDict(frozen=True)
    node_id: str
    transaction_id: str


class WasmExecuteRequest(BaseModel):
    """WASM Sandbox execution request DTO."""

    model_config = ConfigDict(frozen=True)
    patch_code: str
