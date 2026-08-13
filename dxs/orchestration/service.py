from __future__ import annotations

from collections.abc import Callable

from dxs.orchestration.model import ExecutionResult, ExecutionStatus


class OrchestrationService:
    """Coordinates deterministic DXS operations."""

    def execute(
        self,
        name: str,
        operation: Callable[[], str],
    ) -> ExecutionResult:
        try:
            message = operation()

            return ExecutionResult(
                name=name,
                status=ExecutionStatus.COMPLETED,
                message=message,
            )
        except Exception as exc:
            return ExecutionResult(
                name=name,
                status=ExecutionStatus.FAILED,
                message=str(exc),
            )


__all__ = ["OrchestrationService"]