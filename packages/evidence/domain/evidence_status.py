from __future__ import annotations

from enum import StrEnum

"""Domain Enum for Evidence Integrity Status (Item 15 Fix)."""


class EvidenceStatus(StrEnum):
    """Operational integrity status of evidence records."""

    CAPTURED = "CAPTURED"
    VERIFIED = "VERIFIED"
    INVALID = "INVALID"
    TAMPERED = "TAMPERED"
    REJECTED = "REJECTED"
    ARCHIVED = "ARCHIVED"
