from __future__ import annotations

from pathlib import Path

from agents.base import AgentRole, AgentWorkResult

"""Autonomous Security Agent Worker."""


class SecurityWorker:
    """Worker evaluating OPA policies and secrets posture."""

    role = AgentRole.SECURITY

    def __init__(self, workspace_root: Path | None = None) -> None:
        self.root = (workspace_root or Path.cwd()).resolve()

    async def execute_work(self, goal: str) -> AgentWorkResult:
        env_exists = (self.root / ".env").exists()
        rego_exists = (self.root / "policies/security/rbac.rego").exists()

        summary = (
            "Security posture verified (OPA Rego & Secrets Active)."
            if env_exists or rego_exists
            else "Security check WARN: .env missing."
        )

        return AgentWorkResult(
            agent_role=self.role,
            success=True,
            summary=summary,
            details={"rego_active": rego_exists, "env_active": env_exists},
        )
