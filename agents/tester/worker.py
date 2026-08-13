from __future__ import annotations

import subprocess
from pathlib import Path

from agents.base import AgentRole, AgentWorkResult

"""Autonomous Tester Agent Worker."""


class TesterWorker:
    """Worker executing Pytest test suite and collecting evidence."""

    role = AgentRole.TESTER

    def __init__(self, workspace_root: Path | None = None) -> None:
        self.root = (workspace_root or Path.cwd()).resolve()

    async def execute_work(self) -> AgentWorkResult:
        res = subprocess.run(
            ["uv", "run", "task", "test", "-o", "basetemp=runtime/tmp"],
            cwd=str(self.root),
            capture_output=True,
            text=True,
        )
        success = res.returncode == 0
        summary = "Pytest Suite Verified 100% Passed." if success else "Pytest execution FAILED."

        return AgentWorkResult(
            agent_role=self.role,
            success=success,
            summary=summary,
            details={"exit_code": res.returncode},
        )
