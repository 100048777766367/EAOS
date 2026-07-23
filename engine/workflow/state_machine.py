"""Finite State Machine (FSM) workflow engine with stuck auto-rescue."""

from pydantic import BaseModel, ConfigDict


class StateTransitionDTO(BaseModel):
    """Value object representing an FSM state transition."""

    model_config = ConfigDict(frozen=True)

    from_state: str
    to_state: str
    trigger: str


class WorkflowStateDTO(BaseModel):
    """Value object representing active workflow instance state."""

    model_config = ConfigDict(frozen=True)

    instance_id: str
    current_state: str
    stuck_rescued: bool


class FSMWorkflowEngine:
    """Finite State Machine engine executing workflow transitions."""

    def transition_state(
        self,
        instance_id: str,
        current_state: str,
        trigger: str,
    ) -> WorkflowStateDTO:
        """Transitions workflow state and applies auto-rescue if stuck."""
        if trigger == "rescue_stuck":
            return WorkflowStateDTO(
                instance_id=instance_id,
                current_state="RESCUED",
                stuck_rescued=True,
            )

        next_state = "COMPLETED" if trigger == "finish" else "IN_PROGRESS"
        return WorkflowStateDTO(
            instance_id=instance_id,
            current_state=next_state,
            stuck_rescued=False,
        )
