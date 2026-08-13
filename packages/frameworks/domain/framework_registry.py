from __future__ import annotations

import builtins

from pydantic import BaseModel, ConfigDict, Field

from packages.frameworks.domain.models import FrameworkMetadataVO

"""Sprint 3 Engine: Framework & Capability Registry for EAOS."""


class FrameworkRegistry(BaseModel):
    """Registry serving query APIs for all 12 Framework Categories."""

    model_config = ConfigDict(frozen=True)

    frameworks: dict[str, FrameworkMetadataVO] = Field(default_factory=dict)

    @classmethod
    def create_default(cls) -> FrameworkRegistry:
        """Creates a populated default registry instance."""
        fwks = {
            "TOGAF": FrameworkMetadataVO(
                code="TOGAF",
                name="TOGAF Standard",
                category="Enterprise Architecture",
                description="Open Group EA Framework ADM",
            ),
            "BIZBOK": FrameworkMetadataVO(
                code="BIZBOK",
                name="BIZBOK Guide",
                category="Business Architecture",
                description="Business Architecture Guild Body of Knowledge",
            ),
            "APQC": FrameworkMetadataVO(
                code="APQC",
                name="APQC PCF",
                category="Process Architecture",
                description="Process Classification Framework",
            ),
            "SABSA": FrameworkMetadataVO(
                code="SABSA",
                name="SABSA Framework",
                category="Security Architecture",
                description="Security Architecture & Service Management",
            ),
        }
        return cls(frameworks=fwks)

    def list(self) -> builtins.list[str]:
        """Lists all registered framework codes."""
        return builtins.list(self.frameworks.keys())

    def get(self, code: str) -> FrameworkMetadataVO | None:
        """Gets metadata for a specific framework code."""
        return self.frameworks.get(code.upper())

    def find(self, category: str) -> builtins.list[FrameworkMetadataVO]:
        """Finds frameworks belonging to a target category."""
        cat_lower = category.lower()
        return [f for f in self.frameworks.values() if cat_lower in f.category.lower()]


class CapabilityRegistry(BaseModel):
    """Registry mapping Business Capabilities to Frameworks and Rules."""

    model_config = ConfigDict(frozen=True)

    capability_id: str
    bound_frameworks: tuple[str, ...] = ()
    bound_rules: tuple[str, ...] = ()
