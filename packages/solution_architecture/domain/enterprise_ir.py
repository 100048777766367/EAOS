from __future__ import annotations

from enum import StrEnum
from typing import Any

from pydantic import BaseModel, ConfigDict, Field

"""Decoupled Enterprise Intermediate Representation (IR) (Sprint 3.3)."""


class IRNodeType(StrEnum):
    """Node type in Enterprise IR Graph."""

    ENTERPRISE = "ENTERPRISE"
    CAPABILITY = "CAPABILITY"
    ENTITY = "ENTITY"
    POLICY = "POLICY"
    EVENT = "EVENT"


class IRNode(BaseModel):
    """Intermediate Representation Node."""

    model_config = ConfigDict(frozen=True)

    node_id: str = Field(..., description="Node canonical ID")
    node_type: IRNodeType = Field(..., description="IR Node Type")
    label: str = Field(..., description="Display label")
    attributes: dict[str, Any] = Field(default_factory=dict)


class IREdge(BaseModel):
    """Edge linking IR nodes in Enterprise Graph."""

    model_config = ConfigDict(frozen=True)

    source_id: str = Field(..., description="Source node ID")
    target_id: str = Field(..., description="Target node ID")
    relationship: str = Field(..., description="Relationship type")


class EnterpriseIRGraph(BaseModel):
    """Decoupled Enterprise IR Graph representation."""

    model_config = ConfigDict(frozen=True)

    nodes: list[IRNode] = Field(default_factory=list)
    edges: list[IREdge] = Field(default_factory=list)
