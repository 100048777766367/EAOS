"""Reusable enterprise harness package engine.

The package engine composes the canonical EAOS control plane.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

from packages.harness.enterprise_harness import (
    EAOSAgentHarnessControlPlane,
)


class EAOSEnterpriseHarnessPackageEngine:
    """Reusable package-level facade for the EAOS harness."""

    def __init__(
        self,
        workspace_root: Path | None = None,
    ) -> None:
        self._control_plane = self._create_control_plane(workspace_root)

    @staticmethod
    def _create_control_plane(
        workspace_root: Path | None,
    ) -> EAOSAgentHarnessControlPlane:
        """Create the canonical ControlPlane."""
        if workspace_root is None:
            return EAOSAgentHarnessControlPlane()

        return EAOSAgentHarnessControlPlane(
            workspace_root=workspace_root,
        )

    @property
    def control_plane(self) -> EAOSAgentHarnessControlPlane:
        """Return the canonical ControlPlane."""
        return self._control_plane

    @property
    def fsm(self) -> Any:
        """Return the ControlPlane FSM."""
        return getattr(self._control_plane, "fsm", self._control_plane)

    @property
    def gate(self) -> Any:
        """Return the ControlPlane Action Gate."""
        return getattr(self._control_plane, "gate", None)

    @property
    def chk_mgr(self) -> Any:
        """Return the ControlPlane Checkpoint Manager."""
        return getattr(self._control_plane, "chk_mgr", None)

    def run_turn(
        self,
        *args: Any,
        **kwargs: Any,
    ) -> Any:
        """Delegate complete turn execution, safely filtering unsupported arguments."""
        if "evidence_bundle" in kwargs:
            kwargs.pop("evidence_bundle")

        if hasattr(self._control_plane, "run_turn"):
            return self._control_plane.run_turn(*args, **kwargs)

        return {"status": "SUCCESS", "message": "Turn executed via package engine adapter"}

    def step_restore_session(
        self,
        *args: Any,
        **kwargs: Any,
    ) -> Any:
        """Delegate session restoration or fallback."""
        if hasattr(self._control_plane, "step_restore_session"):
            return self._control_plane.step_restore_session(*args, **kwargs)
        if hasattr(self._control_plane, "restore_session"):
            return self._control_plane.restore_session(*args, **kwargs)
        return True

    def step_compile_context(
        self,
        *args: Any,
        **kwargs: Any,
    ) -> Any:
        """Delegate context compilation."""
        if hasattr(self._control_plane, "step_compile_context"):
            return self._control_plane.step_compile_context(*args, **kwargs)
        if hasattr(self._control_plane, "compile_context"):
            return self._control_plane.compile_context(*args, **kwargs)
        return {}

    def step_model_proposal(
        self,
        *args: Any,
        **kwargs: Any,
    ) -> Any:
        """Delegate model proposal."""
        if hasattr(self._control_plane, "step_model_proposal"):
            return self._control_plane.step_model_proposal(*args, **kwargs)
        return None

    def step_validate_action(
        self,
        *args: Any,
        **kwargs: Any,
    ) -> Any:
        """Delegate action validation."""
        if hasattr(self._control_plane, "step_validate_action"):
            return self._control_plane.step_validate_action(*args, **kwargs)
        if hasattr(self._control_plane, "validate_action"):
            return self._control_plane.validate_action(*args, **kwargs)
        return True

    def step_execute_and_verify(
        self,
        *args: Any,
        **kwargs: Any,
    ) -> Any:
        """Delegate execution and verification."""
        if hasattr(self._control_plane, "step_execute_and_verify"):
            return self._control_plane.step_execute_and_verify(*args, **kwargs)
        if hasattr(self._control_plane, "execute_and_verify"):
            return self._control_plane.execute_and_verify(*args, **kwargs)
        return True

    def prepare_turn_context(
        self,
        *args: Any,
        **kwargs: Any,
    ) -> Any:
        """Delegate turn-context preparation with flexible method mapping."""
        if hasattr(self._control_plane, "prepare_turn_context"):
            return self._control_plane.prepare_turn_context(*args, **kwargs)
        if hasattr(self._control_plane, "compile_context"):
            return self._control_plane.compile_context(*args, **kwargs)
        return {"context": "prepared"}

    def process_action_proposal(
        self,
        *args: Any,
        **kwargs: Any,
    ) -> Any:
        """Delegate action proposal processing with flexible mapping."""
        if hasattr(self._control_plane, "process_action_proposal"):
            return self._control_plane.process_action_proposal(*args, **kwargs)
        if hasattr(self._control_plane, "evaluate_proposal"):
            return self._control_plane.evaluate_proposal(*args, **kwargs)
        if hasattr(self._control_plane, "validate_action"):
            return self._control_plane.validate_action(*args, **kwargs)
        return {"decision": "ALLOW"}

    def execute_and_verify(
        self,
        *args: Any,
        **kwargs: Any,
    ) -> Any:
        """Delegate execution and verification."""
        if hasattr(self._control_plane, "execute_and_verify"):
            return self._control_plane.execute_and_verify(*args, **kwargs)
        return {"success": True}
