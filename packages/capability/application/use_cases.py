from pydantic import BaseModel

from packages.capability.domain.models import BusinessCapability
from packages.capability.domain.ports import CapabilityRegistryPort


class LoadCapabilityRequest(BaseModel):
    yaml_content: str


class RegisterCapabilityUseCase:
    """Application Service chịu trách nhiệm biên dịch và nạp năng lực nghiệp vụ."""

    def __init__(self, registry: CapabilityRegistryPort) -> None:
        self.registry = registry

    def execute(self, capability: BusinessCapability) -> BusinessCapability:
        return self.registry.register(capability)
