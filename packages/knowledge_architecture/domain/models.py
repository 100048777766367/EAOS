from __future__ import annotations

from enum import StrEnum
from typing import Any

from pydantic import BaseModel, ConfigDict, Field, computed_field


class NodeCategory(StrEnum):
    CAPABILITY_DOMAIN = "CAPABILITY_DOMAIN"
    SUB_CAPABILITY = "SUB_CAPABILITY"
    BUSINESS_PROCESS = "BUSINESS_PROCESS"
    APPLICATION_COMPONENT = "APPLICATION_COMPONENT"
    DATA_ENTITY = "DATA_ENTITY"
    SERVICE = "SERVICE"


class RelationshipType(StrEnum):
    INCLUDES = "INCLUDES"
    IMPLEMENTS = "IMPLEMENTS"
    DEPENDS_ON = "DEPENDS_ON"
    PRODUCES = "PRODUCES"


class KnowledgeNode(BaseModel):
    model_config = ConfigDict(frozen=True, extra="ignore")

    id: str = Field(description="Unique Canonical Identifier")
    name: str = Field(description="Human readable name")
    category: NodeCategory = Field(description="Architecture Layer/Category")
    properties: dict[str, Any] = Field(default_factory=dict, description="Metadata key-values")


class KnowledgeRelationship(BaseModel):
    model_config = ConfigDict(frozen=True, extra="ignore")

    source_id: str
    target_id: str
    relation: RelationshipType
    properties: dict[str, Any] = Field(default_factory=dict)


class EnterpriseGraphTopology(BaseModel):
    model_config = ConfigDict(frozen=True)

    nodes: list[KnowledgeNode] = Field(default_factory=list)
    relationships: list[KnowledgeRelationship] = Field(default_factory=list)
    total_nodes: int = 0
    total_relationships: int = 0

    @computed_field
    def node_count(self) -> int:
        return self.total_nodes or len(self.nodes)

    @computed_field
    def relationship_count(self) -> int:
        return self.total_relationships or len(self.relationships)
