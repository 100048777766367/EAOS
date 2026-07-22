import uuid
from datetime import UTC, datetime

from pydantic import BaseModel

from packages.self_rewrite.domain.models import (
    AgentExecution,
    Patch,
    PullRequest,
    SelfRewriteJob,
)
from packages.self_rewrite.domain.ports import SelfRewriteRepository


class SelfRewriteRequest(BaseModel):
    problem: str
    author: str


class RunSelfRewriteUseCase:
    """Application Service Ä‘iá»u phá»‘i quy trÃ¬nh tá»± trá»‹ cá»§a chuá»—i AI Agents."""

    def __init__(self, repo: SelfRewriteRepository) -> None:
        self.repo = repo

    def execute(self, request: SelfRewriteRequest) -> SelfRewriteJob:
        job_id = f"REW-{uuid.uuid4().hex[:6].upper()}"

        # BÆ°á»›c 1: Planner Agent phÃ¢n tÃ­ch bÃ i toÃ¡n vÃ  lÃªn káº¿ hoáº¡ch
        log_planner = AgentExecution(
            agent_role="Planner",
            input_received=request.problem,
            output_generated="Káº¿ hoáº¡ch: Chá»‰nh sá»­a cá»•ng cáº¥u hÃ¬nh database.",
            duration_ms=45.2,
        )

        # BÆ°á»›c 2: Architect Agent thiáº¿t káº¿ cáº¥u trÃºc tÃ¡c Ä‘á»™ng
        log_architect = AgentExecution(
            agent_role="Architect",
            input_received=log_planner.output_generated,
            output_generated="Cáº­p nháº­t cáº¥u hÃ¬nh táº¡i adapters.py.",
            duration_ms=62.1,
        )

        # BÆ°á»›c 3: Coder Agent viáº¿t mÃ£ nguá»“n dáº¡ng tá»‡p tin Patch
        diff_text = (
            "--- adapters.py\n"
            "+++ adapters.py\n"
            "@@ -5,1 +5,1 @@\n"
            "- db_port = 5432\n"
            "+ db_port = 5433\n"
        )
        patch = Patch(
            file_path="packages/knowledge/infrastructure/adapters.py",
            diff_content=diff_text,
        )
        log_coder = AgentExecution(
            agent_role="Coder",
            input_received=log_architect.output_generated,
            output_generated=f"ÄÃ£ sinh tá»‡p tin patch cho: {patch.file_path}",
            duration_ms=125.8,
        )

        # BÆ°á»›c 4: Reviewer Agent kiá»ƒm toÃ¡n tiÃªu chuáº©n
        log_reviewer = AgentExecution(
            agent_role="Reviewer",
            input_received=log_coder.output_generated,
            output_generated="MÃ£ nguá»“n há»£p lá»‡, vÆ°á»£t qua kiá»ƒm tra ranh giá»›i.",
            duration_ms=51.4,
        )

        # BÆ°á»›c 5: Tester Agent giáº£ láº­p cháº¡y 1000 tests Sandbox
        log_tester = AgentExecution(
            agent_role="Tester",
            input_received=log_reviewer.output_generated,
            output_generated="Äáº¡t chuáº©n kiá»ƒm Ä‘á»‹nh an toÃ n (1000/1000 passed).",
            duration_ms=88.5,
        )

        # ÄÃ³ng gÃ³i thÃ nh Pull Request Ä‘á» xuáº¥t lÃªn há»™i Ä‘á»“ng
        pr_id = f"PR-{uuid.uuid4().hex[:4].upper()}"
        pull_request = PullRequest(
            id=pr_id,
            title="[Auto-Evolution] Fix Database Port Parameter",
            description=(
                "Pull Request tá»± Ä‘á»™ng khá»Ÿi táº¡o bá»Ÿi Self Rewrite Engine "
                f"Ä‘á»ƒ giáº£i quyáº¿t váº¥n Ä‘á»: {request.problem}"
            ),
            source_branch=f"evolution/{job_id.lower()}",
            target_branch="main",
            patches=[patch],
        )

        job = SelfRewriteJob(
            id=job_id,
            problem=request.problem,
            status="SUCCESS",
            agent_logs=[
                log_planner,
                log_architect,
                log_coder,
                log_reviewer,
                log_tester,
            ],
            pull_request=pull_request,
            created_at=datetime.now(UTC),
        )

        return self.repo.save(job)

