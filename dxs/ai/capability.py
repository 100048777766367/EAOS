from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Capability:
    """Immutable AI capability contract."""

    name: str
    description: str = ""

    def __post_init__(self) -> None:
        name = self.name.strip()

        if not name:
            raise ValueError("Capability name must not be empty.")

        object.__setattr__(self, "name", name)


@dataclass(frozen=True)
class CapabilityRegistrySnapshot:
    """Immutable snapshot of registered AI capabilities."""

    capabilities: tuple[Capability, ...]
