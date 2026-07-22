"""Infrastructure adapters for Traceability repository."""

from pathlib import Path

from packages.traceability.domain.models import TraceabilityChainAggregate
from packages.traceability.domain.ports import TraceabilityRepositoryPort


class InMemoryTraceabilityRepository(TraceabilityRepositoryPort):
    def __init__(self) -> None:
        self._store_by_trace_id: dict[str, TraceabilityChainAggregate] = {}
        self._chains: list[TraceabilityChainAggregate] = []

    def save(self, chain: TraceabilityChainAggregate) -> None:
        self._store_by_trace_id[chain.trace_id] = chain
        self._chains.append(chain)

    def find_by_trace_id(
        self, trace_id: str
    ) -> TraceabilityChainAggregate | None:
        return self._store_by_trace_id.get(trace_id)

    def find_by_location(
        self, file_path: Path, line_number: int
    ) -> TraceabilityChainAggregate | None:
        for chain in self._chains:
            loc = chain.target_location
            if (
                loc.file_path == file_path
                and loc.start_line <= line_number <= loc.end_line
            ):
                return chain
        return None
