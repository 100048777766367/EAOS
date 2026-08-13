"""Deterministic Entity & Relation Graph with PageRank Scoring."""

from __future__ import annotations

from typing import Final

from provenance.domain.models import EntityNodeDTO, RelationEdgeDTO


class DeterministicEntityGraph:
    """Graph engine executing rule-based extraction and PageRank scoring."""

    def __init__(self) -> None:
        self._nodes: Final[dict[str, EntityNodeDTO]] = {}
        self._edges: Final[list[RelationEdgeDTO]] = []

    def add_entity(self, name: str, entity_type: str = "CONCEPT") -> EntityNodeDTO:
        """Adds or updates an entity node in the graph."""
        entity_id = f"ent-{name.lower().replace(' ', '_')}"
        node = EntityNodeDTO(
            entity_id=entity_id,
            name=name,
            entity_type=entity_type,
            pagerank_score=1.0,
        )
        self._nodes[entity_id] = node
        return node

    def add_relation(self, source_id: str, target_id: str, relation_type: str) -> RelationEdgeDTO:
        """Adds a directed relation edge between entities."""
        edge = RelationEdgeDTO(
            source_id=source_id,
            target_id=target_id,
            relation_type=relation_type,
        )
        self._edges.append(edge)
        self._recalculate_pagerank()
        return edge

    def _recalculate_pagerank(self) -> None:
        """Calculates deterministic PageRank scores based on in-degree."""
        in_degrees: dict[str, int] = dict.fromkeys(self._nodes, 0)
        for edge in self._edges:
            if edge.target_id in in_degrees:
                in_degrees[edge.target_id] += 1

        for e_id, count in in_degrees.items():
            old_node = self._nodes[e_id]
            updated_score = 1.0 + (count * 0.5)
            self._nodes[e_id] = old_node.model_copy(update={"pagerank_score": updated_score})

    def get_related_entities(self, entity_id: str, depth: int = 1) -> list[EntityNodeDTO]:
        """Traverses graph to find related entities ordered by PageRank."""
        target_ids: set[str] = {entity_id}
        for _ in range(depth):
            next_targets: set[str] = set()
            for edge in self._edges:
                if edge.source_id in target_ids:
                    next_targets.add(edge.target_id)
                elif edge.target_id in target_ids:
                    next_targets.add(edge.source_id)
            target_ids.update(next_targets)

        results = [self._nodes[e_id] for e_id in target_ids if e_id in self._nodes]
        results.sort(key=lambda x: x.pagerank_score, reverse=True)
        return results
