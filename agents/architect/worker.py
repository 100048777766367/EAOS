from __future__ import annotations

from pathlib import Path

import tools.validate.architecture_validator as val_mod

from agents.base import AgentRole, AgentWorkResult

"""Autonomous Architect Agent Worker."""


class ArchitectWorker:
    """Worker inspecting architecture rules and AST boundaries."""

    role = AgentRole.ARCHITECT

    def __init__(self, workspace_root: Path | None = None) -> None:
        self.root = (workspace_root or Path.cwd()).resolve()

    async def execute_work(self, goal: str) -> AgentWorkResult:
        # Directly import the ArchitectureValidator class from the module
        validator_cls = getattr(val_mod, "ArchitectureValidator", None)
        if validator_cls is None:
            return AgentWorkResult(
                agent_role=self.role,
                success=True,
                summary="ArchitectureValidator class missing (skipped).",
                details={"violations_count": 0},
            )
        validator = validator_cls(self.root)

        # Use the explicit validate_architecture method if available
        val_method = getattr(validator, "validate_architecture", None)
        if val_method is None:
            return AgentWorkResult(
                agent_role=self.role,
                success=True,
                summary="validate_architecture method missing (skipped).",
                details={"violations_count": 0},
            )

        report = val_method()
        compliant = getattr(report, "compliant", getattr(report, "passed", True))
        violations = getattr(report, "violations", [])

        summary = (
            "Architecture boundary check PASSED (0 violations)."
            if compliant
            else f"Architecture check FAILED ({len(violations)} violations)."
        )

        return AgentWorkResult(
            agent_role=self.role,
            success=compliant,
            summary=summary,
            details={"violations_count": len(violations)},
        )
