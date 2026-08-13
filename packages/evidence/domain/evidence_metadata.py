from __future__ import annotations

from typing import Any

from pydantic import BaseModel, ConfigDict, Field

"""Immutable Value Object for Evidence Metadata (Item 9 Fix)."""


class EvidenceMetadata(BaseModel):
    """Immutable Value Object using frozen tuple pairs to prevent mutation."""

    model_config = ConfigDict(frozen=True)

    entries: tuple[tuple[str, str], ...] = Field(default_factory=tuple)

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> EvidenceMetadata:
        """Constructs immutable metadata from dictionary."""
        frozen_entries = tuple((str(k), str(v)) for k, v in data.items())
        return cls(entries=frozen_entries)

    def to_dict(self) -> dict[str, str]:
        """Converts metadata back to dictionary for reading."""
        return dict(self.entries)
