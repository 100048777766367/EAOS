"""Unit tests for the Traceability context."""

from pathlib import Path

from packages.traceability.application.dto import (
    CausalNodeDTO,
    ExplainCodeChangeQuery,
    RecordTraceCommand,
)
from packages.traceability.application.use_cases import (
    ExplainCodeChangeUseCase,
    RecordCodeChangeTraceUseCase,
)
from packages.traceability.domain.models import CausalNodeType
from packages.traceability.infrastructure.adapters import (
    InMemoryTraceabilityRepository,
)


def test_explain_code_change_full_causal_chain() -> None:
    repo = InMemoryTraceabilityRepository()
    record_use_case = RecordCodeChangeTraceUseCase(repo)
    explain_use_case = ExplainCodeChangeUseCase(repo)

    target_file = Path("packages/knowledge/infrastructure/adapters.py")

    cmd = RecordTraceCommand(
        trace_id="TRACE-2026-0722-01",
        file_path=target_file,
        start_line=40,
        end_line=50,
        commit_hash="a1b2c3d4",
        nodes=[
            CausalNodeDTO(
                node_id="SIG-901",
                node_type=CausalNodeType.TELEMETRY_ALERT,
                title="Splay RAM High Latency Alert",
                description="Latency exceeded 450ms threshold under load.",
                evidence_payload={"observed_latency_ms": 450.0},
            ),
            CausalNodeDTO(
                node_id="REF-102",
                node_type=CausalNodeType.REFLECTION_DIAGNOSIS,
                title="Root Cause: Unbounded Splay Tree Growth",
                description="Splay Tree nodes exceeded 1000 without eviction.",
                evidence_payload={"node_count": 1450},
            ),
            CausalNodeDTO(
                node_id="SIM-304",
                node_type=CausalNodeType.SIMULATION_RUN,
                title="Dry-Run Eviction Policy",
                description="1000 tests passed on Sandbox with LRU eviction.",
                evidence_payload={"pass_rate": 1.0},
            ),
            CausalNodeDTO(
                node_id="JOB-505",
                node_type=CausalNodeType.SELF_REWRITE_JOB,
                title="Applied LRU Eviction Patch",
                description="Modified save() in adapters.py to pop oldest key.",
                evidence_payload={"patched_lines": "40-50"},
            ),
        ],
    )

    record_use_case.execute(cmd)

    query = ExplainCodeChangeQuery(file_path=target_file, line_number=42)
    response = explain_use_case.execute(query)

    assert response.found is True
    assert response.trace_id == "TRACE-2026-0722-01"
    assert "Splay RAM High Latency Alert" in response.explanation
    assert "Unbounded Splay Tree Growth" in response.explanation
    assert "Applied LRU Eviction Patch" in response.explanation


def test_explain_code_change_not_found() -> None:
    repo = InMemoryTraceabilityRepository()
    explain_use_case = ExplainCodeChangeUseCase(repo)

    query = ExplainCodeChangeQuery(
        file_path=Path("packages/unknown.py"), line_number=10
    )
    response = explain_use_case.execute(query)

    assert response.found is False
    assert response.trace_id is None
    assert "No AI decision trace found" in response.explanation
