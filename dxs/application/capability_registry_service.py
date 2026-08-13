from __future__ import annotations

from dxs.ai.capability import Capability, CapabilityRegistrySnapshot


class CapabilityRegistryService:
    """Application service for deterministic capability registration."""

    def __init__(
        self,
        capabilities: tuple[Capability, ...] = (),
    ) -> None:
        self._capabilities: dict[str, Capability] = {}

        for capability in capabilities:
            self.register(capability)

    def register(self, capability: Capability) -> None:
        """Register one capability and reject duplicate names."""
        name = capability.name.strip()

        if name in self._capabilities:
            raise ValueError(f"Capability already registered: {name}")

        self._capabilities[name] = capability

    def has(self, name: str) -> bool:
        """Return whether a capability is registered."""
        return name.strip() in self._capabilities

    def get(self, name: str) -> Capability:
        """Return a registered capability."""
        normalized = name.strip()

        try:
            return self._capabilities[normalized]
        except KeyError as exc:
            raise KeyError(f"Capability not registered: {normalized}") from exc

    def list(self) -> tuple[Capability, ...]:
        """Return capabilities in deterministic name order."""
        return tuple(self._capabilities[name] for name in sorted(self._capabilities))

    def snapshot(self) -> CapabilityRegistrySnapshot:
        """Return an immutable registry snapshot."""
        return CapabilityRegistrySnapshot(capabilities=self.list())
