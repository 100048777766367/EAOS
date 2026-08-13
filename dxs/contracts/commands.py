from __future__ import annotations

from collections.abc import Sequence
from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class CommandResult:
    exit_code: int
    message: str
    evidence_path: str | None = None


class Command:
    name: str

    def execute(self, args: Sequence[str]) -> CommandResult:
        raise NotImplementedError
