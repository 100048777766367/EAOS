"""Application use cases for Knowledge Graph context."""

from packages.knowledge_graph.application.dto import (
    AddNodeCommand,
    GraphResponse,
    IngestGraphBatchCommand,
)
from packages.knowledge_graph.domain.models import (
    GraphEdge,
    GraphNode,
    KnowledgeGraphAggregate,
)
from packages.knowledge_graph.domain.ports import (
    KnowledgeGraphRepositoryPort,
)


class IngestKnowledgeGraphUseCase:
    def __init__(self, repository: KnowledgeGraphRepositoryPort) -> None:
        self._repository = repository

    def execute(self, command: IngestGraphBatchCommand) -> GraphResponse:
        graph = self._repository.get_graph(command.graph_id)
        if graph is None:
            graph = KnowledgeGraphAggregate(graph_id=command.graph_id)

        for n_dto in command.nodes:
            lbl = n_dto.label or n_dto.name
            graph.add_node(
                GraphNode(
                    node_id=n_dto.node_id,
                    node_type=n_dto.node_type,
                    label=lbl,
                    properties=n_dto.properties,
                )
            )

        for e_dto in command.edges:
            graph.add_edge(
                GraphEdge(
                    edge_id=e_dto.edge_id,
                    source_node_id=e_dto.source_node_id,
                    target_node_id=e_dto.target_node_id,
                    relationship_type=e_dto.relationship_type,
                )
            )

        self._repository.save(graph)
        return GraphResponse(
            graph_id=graph.graph_id,
            nodes_count=len(graph.nodes),
            edges_count=len(graph.edges),
        )


class ManageKnowledgeGraphUseCase:
    def __init__(self, repository: KnowledgeGraphRepositoryPort) -> None:
        self._repository = repository

    def add_node(self, command: AddNodeCommand) -> GraphResponse:
        graph = self._repository.get_graph(command.graph_id)
        if graph is None:
            graph = KnowledgeGraphAggregate(graph_id=command.graph_id)

        graph.add_node(
            GraphNode(
                node_id=command.node_id,
                node_type=command.node_type,
                label=command.label,
                properties=command.properties,
            )
        )
        self._repository.save(graph)
        return GraphResponse(
            graph_id=graph.graph_id,
            nodes_count=len(graph.nodes),
            edges_count=len(graph.edges),
        )
