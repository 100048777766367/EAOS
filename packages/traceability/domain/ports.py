"""Domain ports for Traceability context."""

from pathlib import Path
from typing import Protocol

from packages.traceability.domain.models import (
    TraceabilityChainAggregate,
)


class TraceabilityRepositoryPort(Protocol):
    def save(self, chain: TraceabilityChainAggregate) -> None: ...

    def find_by_trace_id(self, trace_id: str) -> TraceabilityChainAggregate | None: ...

    def find_by_location(self, file_path: Path, line_number: int) -> TraceabilityChainAggregate | None: ...
