from __future__ import annotations

from dataclasses import dataclass

"""Canonical layers module."""


@dataclass
class CanonicalLayerDTO:
    """Canonical layer DTO."""

    layer_name: str


class CanonicalLayerRegistry:
    """Canonical layer registry."""

    def get_canonical_layers(self) -> list[CanonicalLayerDTO]:
        """Get canonical architecture layers."""
        return [
            CanonicalLayerDTO(layer_name="Core Kernel"),
            CanonicalLayerDTO(layer_name="Domain Services"),
            CanonicalLayerDTO(layer_name="Application Layer"),
            CanonicalLayerDTO(layer_name="Infrastructure Layer"),
        ]
