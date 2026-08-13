from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum


class ValidationStatus(StrEnum):
    PASS = "PASS"
    WARN = "WARN"
    FAIL = "FAIL"


@dataclass(frozen=True, slots=True)
class ValidationResult:
    check: str
    status: ValidationStatus
    message: str
    path: str | None = None

    def to_dict(self) -> dict[str, str | None]:
        return {
            "check": self.check,
            "status": self.status.value,
            "message": self.message,
            "path": self.path,
        }
