from __future__ import annotations

from pathlib import Path

from dxs.application.repository_doctor import RepositoryDoctor
from dxs.bootstrap import create_repository_application
from dxs.contracts.diagnostics import Diagnostic, DiagnosticLevel
from dxs.contracts.evidence import Evidence
from dxs.diagnostics.evidence import write_evidence
from dxs.doctor.context import discover_repository


def run_doctor(
    root: Path | None = None,
) -> tuple[Evidence, Path]:
    repository_root = root.resolve() if root is not None else discover_repository()

    application = create_repository_application()

    results = application.inspect(repository_root)

    diagnostics: list[Diagnostic] = []

    for result in results:
        level = DiagnosticLevel.INFO if result.startswith("[PASS]") else DiagnosticLevel.WARNING

        diagnostics.append(
            Diagnostic(
                code="DXS-DOCTOR",
                level=level,
                message=result,
            )
        )

    status = "passed" if all(diagnostic.level != DiagnosticLevel.ERROR for diagnostic in diagnostics) else "failed"

    evidence = Evidence(
        operation="doctor",
        status=status,
        started_at="",
        completed_at="",
        diagnostics=tuple(diagnostics),
        metadata={
            "repository": str(repository_root),
            "implementation": "RepositoryApplication",
        },
    )

    return evidence, write_evidence(
        evidence,
        repository_root,
    )


__all__ = [
    "RepositoryDoctor",
    "run_doctor",
]
