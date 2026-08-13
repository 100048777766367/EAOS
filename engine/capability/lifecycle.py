import logging

from engine.capability.registry import CapabilityRegistry

"""Lifecycle service managing state enable/disable for capabilities."""


logger = logging.getLogger(__name__)


class CapabilityLifecycleService:
    """Service dedicated strictly to capability activation and lifecycle."""

    def __init__(self, registry: CapabilityRegistry) -> None:
        self.registry = registry
        self._enabled: dict[str, bool] = {}

    def enable(self, capability_id: str) -> None:
        """Enables capability execution."""
        cap_id = capability_id.lower()
        self._enabled[cap_id] = True
        logger.info("Enabled Capability: %s", cap_id)

    def disable(self, capability_id: str) -> None:
        """Disables capability execution."""
        cap_id = capability_id.lower()
        self._enabled[cap_id] = False
        logger.info("Disabled Capability: %s", cap_id)

    def is_enabled(self, capability_id: str) -> bool:
        """Checks if capability is active."""
        cap_id = capability_id.lower()
        return self._enabled.get(cap_id, True)
