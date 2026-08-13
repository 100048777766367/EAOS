import asyncio
from pathlib import Path
from unittest.mock import AsyncMock, Mock

from agents.execution.domain.models import (
    TaskRequest,
    TaskState,
)
from agents.execution.runtime.execution_engine import (
    AgentTaskExecutionEngine,
)


def _run(coro):
    return asyncio.run(coro)


async def _collect_events(
    engine: AgentTaskExecutionEngine,
    request: TaskRequest,
) -> list[dict]:
    return [event async for event in engine.execute(request)]


def _build_engine(tmp_path: Path) -> AgentTaskExecutionEngine:
    (tmp_path / ".eaos").mkdir()

    engine = AgentTaskExecutionEngine(tmp_path)

    engine.guard.prepare = Mock(return_value=Mock(value="PREPARED"))
    engine.guard.snapshot = Mock(return_value="test-revision")

    patch_snapshot = Mock(
        base_revision="test-revision",
        changed=False,
        diff="",
    )
    engine.patch.capture = Mock(return_value=patch_snapshot)

    engine.evidence.store = Mock(return_value="evidence-test")

    return engine


def test_verification_failure_produces_failed_terminal_event(
    tmp_path: Path,
) -> None:
    """FAILED verification must produce FAILED terminal state."""
    engine = _build_engine(tmp_path)

    engine.verification.verify = AsyncMock(
        return_value={
            "result": {
                "status": "FAILED",
                "runs": [
                    {
                        "name": "ruff",
                        "status": "FAILED",
                        "returncode": 1,
                        "output": "verification failed",
                        "error": None,
                    }
                ],
                "evidence_id": "verification-failed",
            }
        }
    )

    request = TaskRequest(
        task_id="task-verification-failure",
        user_request="test verification failure",
        agent_id="coder",
        project_root=tmp_path,
    )

    events = _run(_collect_events(engine, request))

    terminal_events = [event for event in events if event.get("type") == "task_execution_result"]

    assert terminal_events

    terminal = terminal_events[-1]

    assert terminal["state"] == TaskState.FAILED
    assert terminal["payload"]["state"] == "FAILED"
    assert terminal["payload"]["verification_status"] == "FAILED"


def test_verification_pass_produces_completed_terminal_event(
    tmp_path: Path,
) -> None:
    """PASSED verification must produce COMPLETED terminal state."""
    engine = _build_engine(tmp_path)

    engine.verification.verify = AsyncMock(
        return_value={
            "result": {
                "status": "PASSED",
                "runs": [],
                "evidence_id": "verification-passed",
            }
        }
    )

    request = TaskRequest(
        task_id="task-verification-pass",
        user_request="test verification pass",
        agent_id="coder",
        project_root=tmp_path,
    )

    events = _run(_collect_events(engine, request))

    terminal_events = [event for event in events if event.get("type") == "task_execution_result"]

    assert terminal_events

    terminal = terminal_events[-1]

    assert terminal["state"] == TaskState.COMPLETED
    assert terminal["payload"]["state"] == "COMPLETED"
    assert terminal["payload"]["verification_status"] == "PASSED"
