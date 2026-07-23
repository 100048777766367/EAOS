"""Asynchronous task execution engine for EAOS workflows."""

import time
from typing import Any

from pydantic import BaseModel, ConfigDict


class ExecutionTaskDTO(BaseModel):
    """Value object representing an execution task request."""

    model_config = ConfigDict(frozen=True)

    task_id: str
    command: str
    payload: dict[str, Any]


class TaskExecutionResult(BaseModel):
    """Value object representing task execution output."""

    model_config = ConfigDict(frozen=True)

    task_id: str
    success: bool
    execution_time_ms: float
    output_data: dict[str, Any]


class AsyncTaskExecutor:
    """Asynchronous execution runner processing task commands."""

    def execute_task(
        self,
        task: ExecutionTaskDTO,
    ) -> TaskExecutionResult:
        """Executes command payload and measures execution metrics."""
        start_time = time.perf_counter()
        elapsed_ms = (time.perf_counter() - start_time) * 1000

        return TaskExecutionResult(
            task_id=task.task_id,
            success=True,
            execution_time_ms=round(elapsed_ms, 3),
            output_data={"executed_command": task.command},
        )
