from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class DiscoveredCapability:
    """Capability discovered from a known DXS boundary."""

    name: str
    source: str


class CapabilityDiscoveryService:
    """Discover capabilities without executing them."""

    def discover(
        self,
        names: tuple[str, ...],
        source: str,
    ) -> tuple[DiscoveredCapability, ...]:
        """Return deterministic capability descriptors."""
        normalized = sorted({name.strip() for name in names if name.strip()})

        return tuple(
            DiscoveredCapability(
                name=name,
                source=source.strip(),
            )
            for name in normalized
        )
