"""Pytest verification runner."""

from __future__ import annotations

import asyncio
import subprocess
import sys
import time
from pathlib import Path

from ..models import VerificationRun, VerificationStatus


class PytestRunner:
    """Run the EAOS unit-test suite."""

    name = "pytest"

    async def run(
        self,
        project_root: Path,
    ) -> VerificationRun:
        """Run Pytest outside the API event loop."""
        return await asyncio.to_thread(
            self._run_sync,
            project_root,
        )

    def _run_sync(
        self,
        project_root: Path,
    ) -> VerificationRun:
        """Execute Pytest synchronously."""
        command = [
            sys.executable,
            "-m",
            "pytest",
            "tests/unit",
            "-q",
        ]

        started = time.perf_counter()

        try:
            process = subprocess.run(
                command,
                cwd=project_root,
                capture_output=True,
                text=True,
                timeout=300,
                check=False,
            )
        except FileNotFoundError as exc:
            return VerificationRun(
                name=self.name,
                status=VerificationStatus.SKIPPED,
                duration_seconds=time.perf_counter() - started,
                error=str(exc),
            )
        except subprocess.TimeoutExpired:
            return VerificationRun(
                name=self.name,
                status=VerificationStatus.FAILED,
                duration_seconds=time.perf_counter() - started,
                error="Pytest timed out after 300 seconds.",
            )
        except OSError as exc:
            return VerificationRun(
                name=self.name,
                status=VerificationStatus.FAILED,
                duration_seconds=time.perf_counter() - started,
                error=str(exc),
            )

        output = "\n".join(
            part
            for part in (
                process.stdout.strip(),
                process.stderr.strip(),
            )
            if part
        )

        return VerificationRun(
            name=self.name,
            status=(VerificationStatus.PASSED if process.returncode == 0 else VerificationStatus.FAILED),
            returncode=process.returncode,
            output=output[-8000:],
            duration_seconds=time.perf_counter() - started,
        )
