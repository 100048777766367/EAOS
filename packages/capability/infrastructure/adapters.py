from packages.capability.domain.models import BusinessCapability
from packages.capability.domain.ports import CapabilityRegistryPort

"""Infrastructure adapters for capability registry storage."""


class InMemoryCapabilityRegistry(CapabilityRegistryPort):
    """In-memory implementation of CapabilityRegistryPort."""

    def __init__(self) -> None:
        self._capabilities: dict[str, BusinessCapability] = {}

    def register(self, capability: BusinessCapability) -> BusinessCapability:
        """Registers a business capability into in-memory store."""
        self._capabilities[capability.id.lower()] = capability
        return capability

    def find_by_id(self, capability_id: str) -> BusinessCapability | None:
        """Finds business capability by ID."""
        return self._capabilities.get(capability_id.lower())

    def exists(self, capability_id: str) -> bool:
        """Checks if capability exists in memory."""
        return capability_id.lower() in self._capabilities

    def list_all(self) -> list[BusinessCapability]:
        """Lists all registered business capabilities."""
        return list(self._capabilities.values())
