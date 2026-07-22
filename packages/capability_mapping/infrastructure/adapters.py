"""Infrastructure adapters for Capability Mapping."""

from pathlib import Path

from packages.capability_mapping.domain.models import (
    CapabilityMappingAggregate,
)
from packages.capability_mapping.domain.ports import (
    CapabilityMappingRepositoryPort,
    CodebaseScannerPort,
)


class InMemoryCapabilityMappingRepository(CapabilityMappingRepositoryPort):
    def __init__(self) -> None:
        self._store: dict[str, CapabilityMappingAggregate] = {}

    def save(self, mapping: CapabilityMappingAggregate) -> None:
        self._store[mapping.capability_id] = mapping

    def find_by_id(self, capability_id: str) -> CapabilityMappingAggregate | None:
        return self._store.get(capability_id)

    def list_all(self) -> list[CapabilityMappingAggregate]:
        return list(self._store.values())


class FileSystemCodebaseScannerAdapter(CodebaseScannerPort):
    """Scans physical directory structure to verify component existence."""

    def scan_existing_components(self, root_dir: Path) -> set[str]:
        components: set[str] = set()

        packages_dir = root_dir / "packages"
        if packages_dir.exists():
            for p in packages_dir.iterdir():
                if p.is_dir() and not p.name.startswith((".", "_")):
                    components.add(f"packages/{p.name}")

        services_dir = root_dir / "platform_services"
        if services_dir.exists():
            for s in services_dir.iterdir():
                if s.is_dir() and not s.name.startswith((".", "_")):
                    components.add(f"platform_services/{s.name}")

        return components
