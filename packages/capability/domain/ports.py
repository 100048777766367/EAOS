from typing import Protocol

from packages.capability.domain.models import BusinessCapability


class CapabilityRegistryPort(Protocol):
    """Port định nghĩa các hành vi đăng ký và quản lý vòng đời năng lực."""

    def register(self, capability: BusinessCapability) -> BusinessCapability: ...

    def find_by_id(self, cap_id: str) -> BusinessCapability | None: ...

    def list_all(self) -> list[BusinessCapability]: ...
