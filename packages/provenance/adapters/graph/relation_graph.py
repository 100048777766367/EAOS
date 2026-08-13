from __future__ import annotations

from typing import Final

from packages.provenance.domain.entity import Entity
from packages.provenance.domain.relation import Relation

"""Relation Graph Adapter mapping entity relationships to evidence IDs."""


class RelationGraphAdapter:
    """Graph index adapter for relationship view."""

    def __init__(self) -> None:
        self._entities: Final[dict[str, Entity]] = {}
        self._relations: Final[list[Relation]] = []

    def index_entity(self, name: str, entity_type: str = "CONCEPT") -> Entity:
        """Indexes an entity node."""
        e_id = f"ent-{name.lower().replace(' ', '_')}"
        entity = Entity(
            entity_id=e_id,
            canonical_name=name.lower(),
            entity_type=entity_type,
        )
        self._entities[e_id] = entity
        return entity

    def index_relation(
        self,
        source_name: str,
        relation_type: str,
        target_name: str,
        evidence_id: str,
        turn_id: int,
    ) -> Relation:
        """Indexes a directed relation between entities pointing to evidence."""
        e_source = self.index_entity(source_name)
        e_target = self.index_entity(target_name)
        rel_id = f"rel-{len(self._relations) + 1}"

        relation = Relation(
            relation_id=rel_id,
            source_entity_id=e_source.entity_id,
            relation_type=relation_type,
            target_entity_id=e_target.entity_id,
            evidence_id=evidence_id,
            turn_id=turn_id,
        )
        self._relations.append(relation)
        return relation

    def find_evidence_ids_by_entities(self, entity_names: list[str]) -> set[str]:
        """Finds evidence IDs connected to any of the target entity names."""
        names_lower = {n.lower() for n in entity_names}
        target_entity_ids = {e.entity_id for e in self._entities.values() if e.canonical_name in names_lower}

        matched: set[str] = set()
        for rel in self._relations:
            if rel.source_entity_id in target_entity_ids or rel.target_entity_id in target_entity_ids:
                matched.add(rel.evidence_id)

        return matched
