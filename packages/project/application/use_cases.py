import uuid

from packages.project.domain.models import ProjectTask

"""Application use cases for Project Management Capability."""


class CreateProjectTaskUseCase:
    """Use case processing project task creation."""

    def execute(self, project_name: str, title: str) -> ProjectTask:
        """Creates a new project task."""
        t_id = f"TSK-{uuid.uuid4().hex[:8].upper()}"
        return ProjectTask(
            task_id=t_id,
            project_name=project_name,
            title=title,
            status="IN_PROGRESS",
        )
