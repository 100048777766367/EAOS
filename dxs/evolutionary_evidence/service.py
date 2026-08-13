from __future__ import annotations

from .model import EvolutionaryEvidence


class EvolutionaryEvidenceService:
    """Build deterministic evolutionary evidence records."""

    def record(
        self,
        key: str,
        observation: str,
        outcome: str,
    ) -> EvolutionaryEvidence:
        """Record one evolutionary observation."""
        return EvolutionaryEvidence(
            key=key.strip(),
            observation=observation.strip(),
            outcome=outcome.strip(),
        )

    def summarize(
        self,
        evidence: tuple[EvolutionaryEvidence, ...],
    ) -> tuple[str, ...]:
        """Return deterministic evidence summaries."""
        return tuple(
            f"{item.key}: {item.outcome}"
            for item in sorted(
                evidence,
                key=lambda item: item.key,
            )
        )
