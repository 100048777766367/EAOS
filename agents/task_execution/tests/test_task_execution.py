"""Smoke tests for the EAOS task execution subsystem."""

from __future__ import annotations

import asyncio
from pathlib import Path

from agents.task_execution.models import TaskState
from agents.task_execution.task_manager import TaskManager


def test_task_manager_create_and_run(tmp_path: Path) -> None:
    """Verify task lifecycle and execution boundary."""
    manager = TaskManager()
    task = manager.create(
        "Inspect the repository",
        agent_id="coder",
    )

    events = asyncio.run(_collect(manager.run(task, tmp_path)))

    types = [event["type"] for event in events]

    assert types == [
        "task_created",
        "task_planned",
        "task_assigned",
        "task_execution_started",
        "task_execution_result",
        "task_verification_requested",
    ]
    assert task.state is TaskState.VERIFYING
    assert task.result is not None


async def _collect(
    events,
) -> list[dict[str, object]]:
    """Collect async task events."""
    return [event async for event in events]
