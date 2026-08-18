"""In-memory runtime trace recorder."""

from __future__ import annotations

from datetime import UTC, datetime
from typing import Any

from pydantic import BaseModel, ConfigDict, Field

from runtime.traces.quantum_runtime_ledger import QuantumRuntimeLedger


class RuntimeTraceRecord(BaseModel):
    """Recorded runtime trace event."""

    model_config = ConfigDict(frozen=True)

    trace_type: str
    payload: dict[str, Any] = Field(default_factory=dict)
    created_at: str = Field(
        default_factory=lambda: datetime.now(UTC).isoformat()
    )
    proof_hash: str


class TraceEngine:
    """Record runtime trace events with proof hashes."""

    def __init__(self) -> None:
        self._records: list[RuntimeTraceRecord] = []

    def record_trace(
        self,
        trace_type: str,
        payload: dict[str, Any],
    ) -> RuntimeTraceRecord:
        """Record and return a trace event."""
        proof_hash = QuantumRuntimeLedger.generate_trace_proof(
            trace_type,
            payload,
        )
        record = RuntimeTraceRecord(
            trace_type=trace_type,
            payload=payload,
            proof_hash=proof_hash,
        )
        self._records.append(record)
        return record

    def list_records(self) -> list[RuntimeTraceRecord]:
        """Return recorded runtime traces."""
        return list(self._records)
