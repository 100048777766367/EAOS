"""Import tests for Agent Task Execution."""

from agents.execution import (
    AgentTaskService,
    MutationState,
    TaskEvent,
    TaskRequest,
    TaskResult,
    TaskState,
)


def test_public_execution_api() -> None:
    """Public API must import successfully."""
    assert AgentTaskService is not None
    assert TaskState.QUEUED.value == "QUEUED"
    assert MutationState.PREPARED.value == "PREPARED"
    assert TaskEvent is not None
    assert TaskRequest is not None
    assert TaskResult is not None
