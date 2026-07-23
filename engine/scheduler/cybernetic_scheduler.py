"""Cybernetic task scheduler for 3-nested feedback loops."""

import time

from pydantic import BaseModel, ConfigDict


class ScheduledJobDTO(BaseModel):
    """Value object representing a scheduled loop job."""

    model_config = ConfigDict(frozen=True)

    job_id: str
    cadence: str
    command: str


class SchedulerStatusReport(BaseModel):
    """Value object reporting active scheduler jobs."""

    model_config = ConfigDict(frozen=True)

    active_jobs: int
    status: str


class CyberneticLoopScheduler:
    """Scheduler triggering Fast, Medium, and Slow loop tasks."""

    def __init__(self) -> None:
        self._jobs: list[ScheduledJobDTO] = []

    def register_loop_job(
        self,
        cadence: str,
        command: str,
    ) -> SchedulerStatusReport:
        """Registers a periodic feedback loop task."""
        job = ScheduledJobDTO(
            job_id=f"job_{int(time.time())}",
            cadence=cadence,
            command=command,
        )
        self._jobs.append(job)
        return SchedulerStatusReport(
            active_jobs=len(self._jobs),
            status="SCHEDULER_RUNNING",
        )
