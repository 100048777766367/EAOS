"""Basic Agent Task Execution tests."""

from pathlib import Path

from agents.execution.domain.models import (
    MutationState,
    TaskRequest,
    TaskState,
)
from agents.execution.runtime.execution_engine import (
    AgentTaskExecutionEngine,
)


def test_task_request(tmp_path: Path) -> None:
    """Task request must preserve execution identity."""
    request = TaskRequest(
        task_id="task-test",
        user_request="test",
        agent_id="coder",
        project_root=tmp_path,
    )

    assert request.task_id == "task-test"
    assert request.agent_id == "coder"


def test_engine_constructs(tmp_path: Path) -> None:
    """Execution engine must construct."""
    (tmp_path / ".eaos").mkdir()

    engine = AgentTaskExecutionEngine(tmp_path)

    assert engine.project_root == tmp_path.resolve()
    assert MutationState.PREPARED.value == "PREPARED"
    assert TaskState.VERIFYING.value == "VERIFYING"
