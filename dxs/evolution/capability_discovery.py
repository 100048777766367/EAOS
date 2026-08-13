from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class DiscoveredCapability:
    """A capability discovered from the real repository state."""

    name: str
    source: str
    available: bool


class CapabilityDiscovery:
    """Discover evolution-related capabilities from repository state."""

    _PATH_CAPABILITIES: tuple[tuple[str, str], ...] = (
        ("dxs", "dxs"),
        ("ai", "dxs/ai"),
        ("contracts", "dxs/contracts"),
        ("tests", "tests/dxs"),
        ("documentation", "docs"),
        ("governance", "GOVERNANCE.md"),
    )

    def discover(self, root: Path) -> tuple[DiscoveredCapability, ...]:
        """Return deterministic capability discovery results."""
        results: list[DiscoveredCapability] = []

        for name, relative_path in self._PATH_CAPABILITIES:
            path = root / relative_path
            results.append(
                DiscoveredCapability(
                    name=name,
                    source=str(path),
                    available=path.exists(),
                )
            )

        return tuple(results)
