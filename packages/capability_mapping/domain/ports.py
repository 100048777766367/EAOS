"""Domain ports for Capability Mapping context."""

from pathlib import Path
from typing import Protocol

from packages.capability_mapping.domain.models import (
    CapabilityMappingAggregate,
)


class CapabilityMappingRepositoryPort(Protocol):
    def save(self, mapping: CapabilityMappingAggregate) -> None:
        ...

    def find_by_id(
        self, capability_id: str
    ) -> CapabilityMappingAggregate | None:
        ...

    def list_all(self) -> list[CapabilityMappingAggregate]:
        ...


class CodebaseScannerPort(Protocol):
    def scan_existing_components(self, root_dir: Path) -> set[str]:
        """Returns set of relative paths/refs of existing physical components."""
        ...
