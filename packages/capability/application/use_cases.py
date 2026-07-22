from pydantic import BaseModel

from packages.capability.domain.models import BusinessCapability
from packages.capability.domain.ports import CapabilityRegistryPort


class LoadCapabilityRequest(BaseModel):
    yaml_content: str


class RegisterCapabilityUseCase:
    """Application Service chá»‹u trÃ¡ch nhiá»‡m biÃªn dá»‹ch vÃ  náº¡p nÄƒng lá»±c nghiá»‡p vá»¥."""

    def __init__(self, registry: CapabilityRegistryPort) -> None:
        self.registry = registry

    def execute(self, capability: BusinessCapability) -> BusinessCapability:
        return self.registry.register(capability)

