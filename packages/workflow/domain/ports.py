from pathlib import Path
from typing import Protocol

from packages.workflow.domain.models import WorkflowDefinition, WorkflowInstance


class WorkflowRegistryPort(Protocol):
    """Port định nghĩa các hành vi quản lý định nghĩa và phiên chạy quy trình."""

    def register_definition(
        self, definition: WorkflowDefinition
    ) -> WorkflowDefinition: ...

    def find_definition_by_id(
        self, workflow_id: str
    ) -> WorkflowDefinition | None: ...

    def list_definitions(self) -> list[WorkflowDefinition]: ...

    def save_instance(self, instance: WorkflowInstance) -> WorkflowInstance: ...

    def find_instance_by_id(self, instance_id: str) -> WorkflowInstance | None: ...

    def load_from_yaml(self, file_path: Path) -> WorkflowDefinition: ...