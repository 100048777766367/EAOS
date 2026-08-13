"""AI extension boundary for EAOS DXS."""

from .capability import Capability, CapabilityRegistrySnapshot
from .contracts import AIRequest, AIResponse

__all__ = [
    "AIRequest",
    "AIResponse",
    "Capability",
    "CapabilityRegistrySnapshot",
]
