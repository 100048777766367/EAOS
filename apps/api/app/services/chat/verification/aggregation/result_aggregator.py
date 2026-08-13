"""Aggregate independent verification runner results."""

from __future__ import annotations

from ..models import (
    VerificationResult,
    VerificationRun,
    VerificationStatus,
)


class ResultAggregator:
    """Aggregate Ruff/Pytest results."""

    def aggregate(
        self,
        runs: list[VerificationRun],
        evidence_id: str | None = None,
    ) -> VerificationResult:
        """Create the final verification result."""
        if not runs:
            return VerificationResult(
                status=VerificationStatus.SKIPPED,
                runs=(),
                evidence_id=evidence_id,
            )

        failed = any(run.status == VerificationStatus.FAILED for run in runs)

        if failed:
            status = VerificationStatus.FAILED
        elif all(run.status == VerificationStatus.SKIPPED for run in runs):
            status = VerificationStatus.SKIPPED
        else:
            status = VerificationStatus.PASSED

        return VerificationResult(
            status=status,
            runs=tuple(runs),
            evidence_id=evidence_id,
        )
