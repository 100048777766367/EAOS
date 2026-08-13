"""Unit tests verifying EAOS Enterprise Harness Package."""

from typing import Any

import pytest
from packages.harness.domain.actions import ActionIntentDTO
from packages.harness.domain.states import TurnState
from packages.harness.package_engine import EAOSEnterpriseHarnessPackageEngine
from packages.harness.state_machine.turn_state_machine import (
    InvalidStateTransitionError,
)


def test_harness_package_fsm_prevents_illegal_skips() -> None:
    """Verifies state machine matrix blocks invalid skips like CREATED -> COMMITTED."""
    engine = EAOSEnterpriseHarnessPackageEngine()
    assert engine.fsm.state == TurnState.CREATED

    with pytest.raises(InvalidStateTransitionError):
        engine.fsm.transition_to(TurnState.COMMITTED)


def test_harness_package_scope_guard_blocks_out_of_scope() -> None:
    """Verifies Scope Guard blocks target URI outside workspace root."""
    engine = EAOSEnterpriseHarnessPackageEngine()
    intent = ActionIntentDTO(
        action_name="read_file",
        target_uri="C:\\Windows\\System32\\cmd.exe",
    )
    gate_res = engine.gate.evaluate_intent(intent)
    assert gate_res.validated_action is None


def test_harness_package_real_checkpoint_rollback(tmp_path: Any) -> None:
    """Verifies Checkpoint Manager restores exact file contents on rollback."""
    test_file = tmp_path / "apps" / "api" / "app" / "routers" / "chat.py"
    test_file.parent.mkdir(parents=True, exist_ok=True)
    test_file.write_text("PRE_ACTION_CONTENT", encoding="utf-8")

    engine = EAOSEnterpriseHarnessPackageEngine(workspace_root=tmp_path)
    chk = engine.chk_mgr.create_checkpoint(
        session_id="s1",
        turn_id=1,
        files_to_backup=["apps/api/app/routers/chat.py"],
    )

    test_file.write_text("MUTATED_BAD_CONTENT", encoding="utf-8")
    assert test_file.read_text(encoding="utf-8") == "MUTATED_BAD_CONTENT"

    success = engine.chk_mgr.rollback_checkpoint(chk.checkpoint_id)
    assert success is True
    assert test_file.read_text(encoding="utf-8") == "PRE_ACTION_CONTENT"


def test_harness_package_full_turn_lifecycle(tmp_path: Any) -> None:
    """Verifies complete valid run_turn() lifecycle resulting in COMMITTED."""
    engine = EAOSEnterpriseHarnessPackageEngine(workspace_root=tmp_path)
    intent = ActionIntentDTO(
        action_name="edit_file",
        target_uri="apps/api/app/routers/chat.py",
    )

    final_state = engine.run_turn(
        session_id="sess-1",
        turn_id=1,
        user_id="user-A",
        task_text="Fix chat.py",
        intent=intent,
        evidences=[],
        mock_tool_output="Passed 0 errors",
        exit_code=0,
    )

    assert final_state == TurnState.COMMITTED
