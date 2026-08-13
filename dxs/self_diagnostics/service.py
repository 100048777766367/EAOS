from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class DiagnosticFinding:
    """One deterministic self-diagnostic finding."""

    key: str
    passed: bool
    message: str


class SelfDiagnosticsService:
    """Evaluate basic DXS structural health."""

    def inspect_path(
        self,
        key: str,
        path_exists: bool,
    ) -> DiagnosticFinding:
        """Create a structural diagnostic finding."""
        status = "exists" if path_exists else "missing"

        return DiagnosticFinding(
            key=key,
            passed=path_exists,
            message=f"{key}: {status}",
        )
