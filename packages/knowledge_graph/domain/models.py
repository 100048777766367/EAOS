"""Domain models for Knowledge Graph context."""

from dataclasses import dataclass, field
from datetime import UTC, datetime
from enum import Enum, auto


class NodeType(Enum):
    CONCEPT = auto()
    CAPABILITY = auto()
    SERVICE = auto()
    POLICY = auto()
    ARTIFACT = auto()
    EVIDENCE = auto()
    INCIDENT = auto()


@dataclass(frozen=True, slots=True)
class GraphNode:
    node_id: str
    node_type: NodeType
    label: str
    properties: dict[str, str | float | int | bool] = field(
        default_factory=dict
    )


@dataclass(frozen=True, slots=True)
class GraphEdge:
    edge_id: str
    source_node_id: str
    target_node_id: str
    relationship_type: str


@dataclass(slots=True)
class KnowledgeGraphAggregate:
    graph_id: str
    nodes: dict[str, GraphNode] = field(default_factory=dict)
    edges: list[GraphEdge] = field(default_factory=list)
    updated_at: datetime = field(
        default_factory=lambda: datetime.now(UTC)
    )

    def add_node(self, node: GraphNode) -> None:
        self.nodes[node.node_id] = node
        self.updated_at = datetime.now(UTC)

    def add_edge(self, edge: GraphEdge) -> None:
        self.edges.append(edge)
        self.updated_at = datetime.now(UTC)
