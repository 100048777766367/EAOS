"""Data Transfer Objects for Knowledge Graph application layer."""

from pydantic import BaseModel, Field

from packages.knowledge_graph.domain.models import NodeType


class NodeIngestDTO(BaseModel):
    node_id: str
    node_type: NodeType
    label: str = ""
    name: str = ""
    properties: dict[str, str | float | int | bool] = Field(
        default_factory=dict
    )


class EdgeIngestDTO(BaseModel):
    edge_id: str
    source_node_id: str
    target_node_id: str
    relationship_type: str


class IngestGraphBatchCommand(BaseModel):
    graph_id: str
    nodes: list[NodeIngestDTO] = Field(default_factory=list)
    edges: list[EdgeIngestDTO] = Field(default_factory=list)


class AddNodeCommand(BaseModel):
    graph_id: str
    node_id: str
    node_type: NodeType
    label: str
    properties: dict[str, str | float | int | bool] = Field(
        default_factory=dict
    )


class AddEdgeCommand(BaseModel):
    graph_id: str
    edge_id: str
    source_node_id: str
    target_node_id: str
    relationship_type: str


class GraphResponse(BaseModel):
    graph_id: str
    nodes_count: int
    edges_count: int
