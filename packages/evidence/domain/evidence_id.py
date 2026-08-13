from __future__ import annotations

import re
from typing import Any

from pydantic import BaseModel, ConfigDict, Field

"""Value Object for Evidence ID Formatting and Validation (Rule R48)."""


class InvalidEvidenceIdFormatError(Exception):
    """Raised when evidence ID string fails format validation."""


class EvidenceId(BaseModel):
    """Immutable Value Object representing a validated Evidence ID."""

    model_config = ConfigDict(frozen=True)

    value: str = Field(..., description="Enterprise semantic model field description")

    def __init__(self, **data: Any) -> None:
        super().__init__(**data)
        if not re.match(r"^E-[0-9A-Fa-f]{8,}$", self.value):
            raise InvalidEvidenceIdFormatError(
                f"Invalid Evidence ID format '{self.value}'. Must match pattern 'E-XXXXXXXX' (min 8 hex chars)."
            )

    def __str__(self) -> str:
        return self.value
