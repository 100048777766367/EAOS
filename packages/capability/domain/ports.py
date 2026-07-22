from typing import Protocol

from packages.capability.domain.models import BusinessCapability


class CapabilityRegistryPort(Protocol):
    """Port Ä‘á»‹nh nghÄ©a cÃ¡c hÃ nh vi Ä‘Äƒng kÃ½ vÃ  quáº£n lÃ½ vÃ²ng Ä‘á»i nÄƒng lá»±c."""

    def register(self, capability: BusinessCapability) -> BusinessCapability: ...

    def find_by_id(self, cap_id: str) -> BusinessCapability | None: ...

    def list_all(self) -> list[BusinessCapability]: ...

