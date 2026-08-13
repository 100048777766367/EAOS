from pydantic import BaseModel, ConfigDict, Field

"""Sprint 4 Engine: EA Knowledge Graph for AI Reasoning."""


class GraphNodeVO(BaseModel):
    """Value object representing a node in the EA Knowledge Graph."""

    model_config = ConfigDict(frozen=True)

    node_id: str
    node_type: str  # Framework, Capability, Process, Rule, Code
    name: str


class GraphEdgeVO(BaseModel):
    """Value object representing a directed edge in Knowledge Graph."""

    model_config = ConfigDict(frozen=True)

    source_id: str
    target_id: str
    relation: str


class EAKnowledgeGraphEngine(BaseModel):
    """Knowledge Graph Engine executing graph traversals for ai."""

    model_config = ConfigDict(frozen=True)

    nodes: dict[str, GraphNodeVO] = Field(default_factory=dict)
    edges: tuple[GraphEdgeVO, ...] = ()

    def traverse_path(self, start_id: str) -> list[str]:
        """Traverses edges connected to start node."""
        return [e.target_id for e in self.edges if e.source_id == start_id]
