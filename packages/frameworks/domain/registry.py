"""Framework Runtime & Knowledge Graph Domain Models for EAOS."""

from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field

from packages.frameworks.domain.models import EAFrameworkType


class GraphNodeVO(BaseModel):
    """Value object representing a node in the EA Knowledge Graph."""

    model_config = ConfigDict(frozen=True)

    node_id: str = Field(..., description="Unique Node ID")
    node_type: str = Field(..., description="Framework, Principle, etc.")
    name: str
    properties: dict[str, str] = Field(default_factory=dict)


class GraphEdgeVO(BaseModel):
    """Value object representing a directed edge in Knowledge Graph."""

    model_config = ConfigDict(frozen=True)

    source_id: str
    target_id: str
    relation_type: str


class FrameworkConceptVO(BaseModel):
    """Value object representing a concept within an EA framework."""

    model_config = ConfigDict(frozen=True)

    concept_id: str = Field(..., description="Unique Concept ID")
    framework: EAFrameworkType
    name: str
    category: str
    mapped_eaos_capability: str | None = None


class FrameworkRegistry(BaseModel):
    """Runtime registry maintaining all loaded EA frameworks."""

    model_config = ConfigDict(frozen=True)

    version: str = "3.0.0"
    concepts: dict[str, FrameworkConceptVO] = Field(default_factory=dict)

    def register_concept(self, concept: FrameworkConceptVO) -> FrameworkRegistry:
        """Registers a framework concept into the registry."""
        new_concepts = dict(self.concepts)
        new_concepts[concept.concept_id] = concept
        return FrameworkRegistry(version=self.version, concepts=new_concepts)
