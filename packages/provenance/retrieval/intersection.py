from __future__ import annotations

"""Deterministic Dual View Intersection Engine (Temporal Candidates ∩ Relation Candidates)."""


class DualViewIntersectionEngine:
    """Intersects relation candidates and temporal candidates deterministically."""

    def intersect_views(
        self,
        relation_candidates: set[str],
        temporal_candidates: set[str],
    ) -> set[str]:
        """Performs Temporal Candidates ∩ Relation Candidates intersection."""
        if relation_candidates and temporal_candidates:
            intersected = temporal_candidates.intersection(relation_candidates)
            return intersected if intersected else temporal_candidates

        if temporal_candidates:
            return temporal_candidates

        return relation_candidates
