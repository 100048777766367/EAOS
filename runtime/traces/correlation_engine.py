"""Runtime correlation context creation."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime
from uuid import uuid4

from runtime.traces.quantum_runtime_ledger import QuantumRuntimeLedger


@dataclass(frozen=True)
class CorrelationContext:
    """Stable correlation metadata for one runtime task."""

    task_id: str
    correlation_id: str
    user_request_id: str | None
    agent_id: str
    created_at: str = field(
        default_factory=lambda: datetime.now(UTC).isoformat()
    )

    def generate_proof_hash(self) -> str:
        """Generate a proof hash for this correlation context."""
        return QuantumRuntimeLedger.generate_trace_proof(
            "CORRELATION_CONTEXT",
            {
                "agent_id": self.agent_id,
                "correlation_id": self.correlation_id,
                "created_at": self.created_at,
                "task_id": self.task_id,
                "user_request_id": self.user_request_id,
            },
        )


class CorrelationEngine:
    """Create runtime correlation contexts."""

    def __init__(self) -> None:
        self._contexts: dict[str, CorrelationContext] = {}

    def create_context(
        self,
        user_request_id: str | None = None,
        agent_id: str = "agent-eaos-core",
        task_id: str | None = None,
    ) -> CorrelationContext:
        """Create a fresh task correlation context."""
        correlation_id = f"corr-{uuid4().hex}"
        context = CorrelationContext(
            task_id=task_id or f"tsk-{uuid4().hex}",
            correlation_id=correlation_id,
            user_request_id=user_request_id,
            agent_id=agent_id,
        )
        self._contexts[context.task_id] = context
        return context

    def get_context(
        self,
        task_id: str,
    ) -> CorrelationContext | None:
        """Return a previously created correlation context."""
        return self._contexts.get(task_id)
