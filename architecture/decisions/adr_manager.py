from __future__ import annotations

from dataclasses import dataclass

"""ADR manager module."""


@dataclass
class ADRRecordDTO:
    """ADR Record DTO."""

    adr_id: str = "ADR-UI-001"
    title: str = "Adopt Micro-Frontends"


class ADRManager:
    """ADR manager implementation."""

    def list_adrs(self) -> list[ADRRecordDTO]:
        """List ratified ADR records."""
        return [
            ADRRecordDTO(adr_id="ADR-UI-001"),
            ADRRecordDTO(adr_id="ADR-SEC-002"),
            ADRRecordDTO(adr_id="ADR-DATA-003"),
        ]


AdrManager = ADRManager
