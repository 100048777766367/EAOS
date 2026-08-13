from __future__ import annotations

from dataclasses import replace
from datetime import UTC, datetime

from .model import Evidence, EvidenceStatus


class EvidenceService:
    """Deterministic evidence lifecycle service."""

    def capture(
        self,
        key: str,
        value: str,
        source: str,
    ) -> Evidence:
        """Capture new repository evidence."""
        return Evidence(
            key=key.strip(),
            value=value,
            source=source.strip(),
            status=EvidenceStatus.OPEN,
            created_at=datetime.now(UTC),
        )

    def verify(self, evidence: Evidence) -> Evidence:
        """Mark evidence as verified."""
        return replace(
            evidence,
            status=EvidenceStatus.VERIFIED,
        )

    def supersede(self, evidence: Evidence) -> Evidence:
        """Mark evidence as superseded."""
        return replace(
            evidence,
            status=EvidenceStatus.SUPERSEDED,
        )
