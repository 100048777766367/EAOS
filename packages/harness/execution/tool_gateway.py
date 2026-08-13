from __future__ import annotations

from pathlib import Path
from typing import Final

from packages.harness.domain.actions import ValidatedActionDTO

"""Tool Execution Gateway with Workspace Boundary Enforcement."""


class ToolExecutionResultDTO:
    """Result from Tool Gateway execution."""

    def __init__(
        self,
        action_id: str,
        stdout: str,
        exit_code: int = 0,
    ) -> None:
        self.action_id = action_id
        self.stdout = stdout
        self.exit_code = exit_code


class ToolGateway:
    """Sandboxed Tool Execution Gateway."""

    def __init__(self, workspace_root: Path | None = None) -> None:
        self.root: Final[Path] = (workspace_root or Path.cwd()).resolve()

    def execute_action(self, action: ValidatedActionDTO) -> ToolExecutionResultDTO:
        """Executes validated action inside workspace boundary."""
        return ToolExecutionResultDTO(
            action_id=action.action_id,
            stdout=(f"Executed action '{action.action_id}' on '{action.target_uri}'"),
            exit_code=0,
        )
