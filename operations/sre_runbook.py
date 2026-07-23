"""Operational SRE runbook engine and incident response manager."""

from pydantic import BaseModel, ConfigDict


class RunbookTaskDTO(BaseModel):
    """Value object representing an SRE operational runbook task."""

    model_config = ConfigDict(frozen=True)

    task_id: str
    command: str
    target_service: str


class OperationalRunbookEngine:
    """Engine executing operational runbooks, SRE tasks, and FinOps actions."""

    def get_active_runbooks(self) -> list[RunbookTaskDTO]:
        """Returns list of automated operational SRE runbooks."""
        return [
            RunbookTaskDTO(
                task_id="SRE-RUNBOOK-01",
                command="uv run task loop EXECUTION",
                target_service="EAOS Gateway",
            ),
            RunbookTaskDTO(
                task_id="SRE-RUNBOOK-02",
                command="uv run task time_machine record prod_checkpoint",
                target_service="Time Machine",
            ),
        ]
