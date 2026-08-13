from __future__ import annotations

from dataclasses import dataclass

from .diagnostics import Diagnostic


@dataclass(frozen=True, slots=True)
class ValidationResult:
    passed: bool
    diagnostics: tuple[Diagnostic, ...] = ()
