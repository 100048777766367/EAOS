"""Domain models for Traceability context."""

from dataclasses import dataclass, field
from datetime import UTC, datetime
from enum import Enum, auto
from pathlib import Path


class CausalNodeType(Enum):
    TELEMETRY_ALERT = auto()
    REFLECTION_DIAGNOSIS = auto()
    LEARNED_EXPERIENCE = auto()
    PREDICTED_RISK = auto()
    SIMULATION_RUN = auto()
    SELF_REWRITE_JOB = auto()
    COUNCIL_VOTE = auto()
    GIT_PATCH_COMMIT = auto()


@dataclass(frozen=True, slots=True)
class CodeLocation:
    file_path: Path
    start_line: int
    end_line: int
    commit_hash: str | None = None


@dataclass(frozen=True, slots=True)
class CausalNode:
    node_id: str
    node_type: CausalNodeType
    title: str
    description: str
    evidence_payload: dict[str, str | float | int | bool]
    created_at: datetime = field(
        default_factory=lambda: datetime.now(UTC)
    )


@dataclass(slots=True)
class TraceabilityChainAggregate:
    trace_id: str
    target_location: CodeLocation
    nodes: list[CausalNode] = field(default_factory=list)

    def add_causal_node(self, node: CausalNode) -> None:
        self.nodes.append(node)

    def generate_explanation(self) -> str:
        """Constructs a human-and-AI-readable causal explanation."""
        if not self.nodes:
            return (
                f"No traceability data found for "
                f"{self.target_location.file_path}:{self.target_location.start_line}."
            )

        lines = [
            f"=== CAUSAL TRACEABILITY REPORT FOR TRACE ID: {self.trace_id} ===",
            f"Target File: {self.target_location.file_path}",
            f"Lines: {self.target_location.start_line}-{self.target_location.end_line}",
            f"Commit: {self.target_location.commit_hash or 'PENDING_COMMIT'}",
            "\nCausal Decision Chain (From Trigger to Code Change):",
        ]

        for index, node in enumerate(self.nodes, start=1):
            lines.append(
                f" [{index}] [{node.node_type.name}] ID: {node.node_id}\n"
                f"     Title: {node.title}\n"
                f"     Reason: {node.description}\n"
                f"     Evidence: {node.evidence_payload}"
            )

        return "\n".join(lines)
