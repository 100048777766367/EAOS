"""Domain ports for Knowledge Graph context."""

from typing import Protocol

from packages.knowledge_graph.domain.models import KnowledgeGraphAggregate


class KnowledgeGraphRepositoryPort(Protocol):
    def save(self, graph: KnowledgeGraphAggregate) -> None: ...

    def get_graph(self, graph_id: str) -> KnowledgeGraphAggregate | None: ...
