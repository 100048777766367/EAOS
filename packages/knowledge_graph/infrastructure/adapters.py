"""Infrastructure adapters for Knowledge Graph context."""

from packages.knowledge_graph.domain.models import KnowledgeGraphAggregate
from packages.knowledge_graph.domain.ports import (
    KnowledgeGraphRepositoryPort,
)


class InMemoryKnowledgeGraphAdapter(KnowledgeGraphRepositoryPort):
    def __init__(self) -> None:
        self._graphs: dict[str, KnowledgeGraphAggregate] = {}

    def save(self, graph: KnowledgeGraphAggregate) -> None:
        self._graphs[graph.graph_id] = graph

    def get_graph(
        self, graph_id: str
    ) -> KnowledgeGraphAggregate | None:
        return self._graphs.get(graph_id)

    def find_by_id(
        self, graph_id: str
    ) -> KnowledgeGraphAggregate | None:
        return self.get_graph(graph_id)


InMemoryKnowledgeGraphRepository = InMemoryKnowledgeGraphAdapter
