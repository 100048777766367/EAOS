from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

"""Capability registry module."""


@dataclass
class CapabilitySpecDTO:
    """Capability spec DTO."""

    capability_id: str
    has_api_spec: bool = True
    has_domain_spec: bool = True


class CapabilityRegistryEngine:
    """Capability registry engine."""

    def __init__(self, workspace_root: Path | None = None) -> None:
        self.workspace_root = workspace_root or Path(".")

    def scan_all_capabilities(self) -> list[CapabilitySpecDTO]:
        """Scan capabilities catalog."""
        cap_dir = self.workspace_root / "capabilities"
        results: list[CapabilitySpecDTO] = []
        if cap_dir.exists():
            for child in cap_dir.iterdir():
                if child.is_dir():
                    has_api = (child / "api.yaml").exists() or (child / "api.json").exists()
                    has_domain = (child / "domain.md").exists() or (child / "domain.yaml").exists()
                    results.append(
                        CapabilitySpecDTO(
                            capability_id=child.name,
                            has_api_spec=has_api,
                            has_domain_spec=has_domain,
                        )
                    )
        if not results:
            results.append(CapabilitySpecDTO(capability_id="default"))
        return results


CapabilityRegistry = CapabilityRegistryEngine
