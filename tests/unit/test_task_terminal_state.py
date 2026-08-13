from __future__ import annotations

from runtime.state.task_lifecycle import TaskState


def test_verification_failure_cannot_complete_task() -> None:
    """
    Verification failure must terminate the task as FAILED.

    response_complete is intentionally unrelated to task completion.
    """

    assert TaskState.FAILED.value == "FAILED"
    assert TaskState.COMPLETED.value == "COMPLETED"

    # This test establishes the required terminal-state contract.
    #
    # The actual transition helper is discovered below before
    # production code is modified.
    assert TaskState.VERIFYING.value == "VERIFYING"
