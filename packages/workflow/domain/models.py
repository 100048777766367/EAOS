"""Workflow state machine domain entities and value objects."""

from typing import Any

from pydantic import BaseModel, ConfigDict


class Transition(BaseModel):
    """Value object representing a workflow state transition rule."""

    model_config = ConfigDict(frozen=True)

    trigger: str
    target: str


class State(BaseModel):
    """Value object representing a workflow state definition."""

    model_config = ConfigDict(frozen=True)

    name: str
    transitions: list[Transition] = []


class WorkflowDefinition(BaseModel):
    """Aggregate root representing a workflow definition."""

    model_config = ConfigDict(frozen=True)

    id: str
    name: str
    initial_state: str
    states: list[State] = []


class WorkflowState(BaseModel):
    """Value object representing active workflow state."""

    model_config = ConfigDict(frozen=True)

    state_name: str
    is_terminal: bool


class WorkflowInstance(BaseModel):
    """Value object representing active workflow instance execution."""

    model_config = ConfigDict(frozen=True)

    instance_id: str
    workflow_id: str = ""
    definition_id: str = ""
    current_state: str
    history: list[str] = []
    metadata: dict[str, Any] = {}
