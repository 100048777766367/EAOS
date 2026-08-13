from typing import Any

from packages.capability.compat.capability import BusinessCapability
from packages.shared.governance.deprecation import deprecated_api

from engine.capability.lifecycle import CapabilityLifecycleService
from engine.capability.registry import CapabilityRegistry

"""Compatibility adapter mapping legacy registry callers to new services."""


class CapabilityCompatibilityAdapter:
    """Adapter bridging legacy registry interface to core registry & lifecycle."""

    def __init__(
        self,
        registry: CapabilityRegistry,
        lifecycle: CapabilityLifecycleService | None = None,
    ) -> None:
        self.registry = registry
        self.lifecycle = lifecycle or CapabilityLifecycleService(registry)

    def register(self, plugin: Any) -> None:
        """Delegates registration to core registry."""
        self.registry.register(plugin)

    @deprecated_api(since="3.0.0", remove_in="4.0.0", replacement="resolve")
    def find_by_id(self, capability_id: str) -> BusinessCapability | None:
        """Legacy method finding capability as BusinessCapability object."""
        res = self.registry.resolve(capability_id)
        if not res:
            return None
        if isinstance(res, BusinessCapability):
            return res
        cap_id = str(getattr(res, "capability_id", capability_id))
        version = str(getattr(res, "version", "1.0.0"))
        return BusinessCapability(
            id=cap_id,
            name=cap_id.capitalize(),
            status="active",
            version=version,
        )

    @deprecated_api(since="3.0.0", remove_in="4.0.0", replacement="resolve")
    def list_all(self) -> list[BusinessCapability]:
        """Legacy method returning list of BusinessCapabilities."""
        result: list[BusinessCapability] = []
        for cap_id in self.registry._plugins:
            bc = self.find_by_id(cap_id)
            if bc:
                result.append(bc)
        return result
