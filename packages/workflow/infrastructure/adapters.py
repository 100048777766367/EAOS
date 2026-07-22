from pathlib import Path
from typing import Any

import yaml  # type: ignore[import-untyped]

from packages.workflow.domain.models import (
    State,
    Transition,
    WorkflowDefinition,
    WorkflowInstance,
)
from packages.workflow.domain.ports import WorkflowRegistryPort


class InMemoryWorkflowRegistry(WorkflowRegistryPort):
    def __init__(self) -> None:
        self._definitions: dict[str, WorkflowDefinition] = {}
        self._instances: dict[str, WorkflowInstance] = {}

    def register_definition(
        self, definition: WorkflowDefinition
    ) -> WorkflowDefinition:
        self._definitions[definition.id] = definition
        return definition

    def find_definition_by_id(
        self, workflow_id: str
    ) -> WorkflowDefinition | None:
        return self._definitions.get(workflow_id)

    def list_definitions(self) -> list[WorkflowDefinition]:
        return list(self._definitions.values())

    def save_instance(self, instance: WorkflowInstance) -> WorkflowInstance:
        self._instances[instance.instance_id] = instance
        return instance

    def find_instance_by_id(self, instance_id: str) -> WorkflowInstance | None:
        return self._instances.get(instance_id)

    def load_from_yaml(self, file_path: Path) -> WorkflowDefinition:
        if not file_path.exists():
            raise FileNotFoundError(f"Không tìm thấy tệp workflow: {file_path}")

        content = file_path.read_text(encoding="utf-8")
        data: dict[str, Any] = yaml.safe_load(content)

        states = []
        for s in data.get("states", []):
            transitions = [
                Transition(
                    trigger=str(t.get("trigger", "")),
                    target=str(t.get("target", "")),
                )
                for t in s.get("transitions", [])
            ]
            states.append(
                State(
                    name=str(s.get("name", "")),
                    transitions=transitions,
                )
            )

        return WorkflowDefinition(
            id=str(data.get("id", "workflow.unknown")),
            name=str(data.get("name", "Unknown Workflow")),
            initial_state=str(data.get("initial_state", "drafted")),
            states=states,
        )
