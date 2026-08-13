from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field

"""Ecosystem Multi-Enterprise Capability Marketplace."""


class PublishedCapabilityDTO(BaseModel):
    """Value object representing a published capability in marketplace."""

    model_config = ConfigDict(frozen=True)

    capability_id: str
    title: str
    publisher_enterprise_id: str
    version: str = Field(default="1.0.0")


class EcosystemCapabilityMarketplace:
    """Marketplace for publishing and discovering capabilities."""

    def list_published_capabilities(self) -> list[PublishedCapabilityDTO]:
        """Return published capability listings."""
        return [
            PublishedCapabilityDTO(
                capability_id="cap-quantum-security",
                title="Post-Quantum Security Capability",
                publisher_enterprise_id="ent-node-01",
            )
        ]
