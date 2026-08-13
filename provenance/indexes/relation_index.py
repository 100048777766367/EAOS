"""Lightweight Relation Index (Relation View)."""

from __future__ import annotations

from typing import Final

from provenance.domain.models import RelationIndexDTO


class RelationIndex:
    """Index mapping entity relationships to Raw Evidence IDs."""

    def __init__(self) -> None:
        self._indexes: Final[list[RelationIndexDTO]] = []

    def index_relation(
        self,
        source_entity: str,
        target_entity: str,
        relation_type: str,
        evidence_id: str,
    ) -> RelationIndexDTO:
        """Adds a light relation index entry pointing to raw evidence."""
        entry = RelationIndexDTO(
            source_entity=source_entity.lower(),
            target_entity=target_entity.lower(),
            relation_type=relation_type,
            evidence_id=evidence_id,
        )
        self._indexes.append(entry)
        return entry

    def find_evidence_ids(self, entity_name: str) -> set[str]:
        """Finds raw evidence IDs connected to an entity name."""
        entity_lower = entity_name.lower()
        matched: set[str] = set()
        for idx in self._indexes:
            if idx.source_entity == entity_lower or idx.target_entity == entity_lower:
                matched.add(idx.evidence_id)
        return matched
