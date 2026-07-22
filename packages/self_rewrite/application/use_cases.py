"""Application use cases for Self Rewrite context."""

import uuid
from datetime import UTC, datetime

from packages.self_rewrite.application.dto import SelfRewriteRequest
from packages.self_rewrite.domain.models import (
    AgentExecution,
    Patch,
    PullRequest,
    SelfRewriteJob,
)
from packages.self_rewrite.domain.ports import SelfRewriteRepository

__all__ = ["RunSelfRewriteUseCase", "SelfRewriteRequest"]


class RunSelfRewriteUseCase:
    """Application Service orchestrating AI agent code generation."""

    def __init__(self, repo: SelfRewriteRepository) -> None:
        self.repo = repo

    def execute(self, request: SelfRewriteRequest) -> SelfRewriteJob:
        job_id = f"REW-{uuid.uuid4().hex[:6].upper()}"

        log_planner = AgentExecution(
            agent_role="Planner",
            input_received=request.problem,
            output_generated="Plan: Patch database connection settings.",
            duration_ms=45.2,
        )

        patch = Patch(
            file_path="packages/knowledge/infrastructure/adapters.py",
            diff_content="--- adapters.py\n+++ adapters.py\n",
        )

        pr_id = f"PR-{uuid.uuid4().hex[:4].upper()}"
        pull_request = PullRequest(
            id=pr_id,
            title="[Auto-Evolution] Fix Config Parameter",
            description=f"Auto-generated PR for: {request.problem}",
            source_branch=f"evolution/{job_id.lower()}",
            target_branch="main",
            patches=[patch],
        )

        job = SelfRewriteJob(
            id=job_id,
            problem=request.problem,
            status="SUCCESS",
            agent_logs=[log_planner],
            pull_request=pull_request,
            created_at=datetime.now(UTC),
        )

        return self.repo.save(job)
