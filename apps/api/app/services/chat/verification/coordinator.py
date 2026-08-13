"""Application coordinator for EAOS verification."""

from __future__ import annotations

from collections.abc import AsyncGenerator
from pathlib import Path
from typing import Any

from .aggregation.result_aggregator import ResultAggregator
from .evidence.evidence_store import EvidenceStore
from .models import VerificationRun
from .runners.pytest_runner import PytestRunner
from .runners.ruff_runner import RuffRunner


class VerificationCoordinator:
    """Coordinate verification runners and evidence."""

    def __init__(self, project_root: Path) -> None:
        """Initialize verification coordinator."""
        self.project_root = project_root.resolve()
        self.runners = (
            RuffRunner(),
            PytestRunner(),
        )
        self.aggregator = ResultAggregator()
        self.evidence = EvidenceStore(self.project_root)

    async def run(
        self,
    ) -> AsyncGenerator[dict[str, Any], None]:
        """Run verification and stream operational events."""
        yield {
            "type": "verification_started",
            "message": "Verification started",
            "runners": [runner.name for runner in self.runners],
        }

        runs: list[VerificationRun] = []

        for runner in self.runners:
            yield {
                "type": "verification_runner_started",
                "runner": runner.name,
            }

            result = await runner.run(self.project_root)
            runs.append(result)

            yield {
                "type": "verification_runner_result",
                "runner": result.name,
                "status": result.status.value,
                "returncode": result.returncode,
                "duration_seconds": result.duration_seconds,
                "output": result.output,
                "error": result.error,
            }

        preliminary = self.aggregator.aggregate(runs)

        evidence_id = self.evidence.store(
            preliminary.as_dict(),
        )

        final = self.aggregator.aggregate(
            runs,
            evidence_id=evidence_id,
        )

        yield {
            "type": "verification_result",
            "status": final.status.value,
            "result": final.as_dict(),
        }
