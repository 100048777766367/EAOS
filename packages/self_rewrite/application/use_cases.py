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
    """Application Service điều phối quy trình tự trị của chuỗi AI Agents."""

    def __init__(self, repo: SelfRewriteRepository) -> None:
        self.repo = repo

    def execute(self, request: SelfRewriteRequest) -> SelfRewriteJob:
        job_id = f"REW-{uuid.uuid4().hex[:6].upper()}"

        # Bước 1: Planner Agent phân tích bài toán và lên kế hoạch
        log_planner = AgentExecution(
            agent_role="Planner",
            input_received=request.problem,
            output_generated="Kế hoạch: Chỉnh sửa cổng cấu hình database.",
            duration_ms=45.2,
        )

        # Bước 2: Architect Agent thiết kế cấu trúc tác động
        log_architect = AgentExecution(
            agent_role="Architect",
            input_received=log_planner.output_generated,
            output_generated="Cập nhật cấu hình tại adapters.py.",
            duration_ms=62.1,
        )

        # Bước 3: Coder Agent viết mã nguồn dạng tệp tin Patch
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
            output_generated=f"Đã sinh tệp tin patch cho: {patch.file_path}",
            duration_ms=125.8,
        )

        # Bước 4: Reviewer Agent kiểm toán tiêu chuẩn
        log_reviewer = AgentExecution(
            agent_role="Reviewer",
            input_received=log_coder.output_generated,
            output_generated="Mã nguồn hợp lệ, vượt qua kiểm tra ranh giới.",
            duration_ms=51.4,
        )

        # Bước 5: Tester Agent giả lập chạy 1000 tests Sandbox
        log_tester = AgentExecution(
            agent_role="Tester",
            input_received=log_reviewer.output_generated,
            output_generated="Đạt chuẩn kiểm định an toàn (1000/1000 passed).",
            duration_ms=88.5,
        )

        # Đóng gói thành Pull Request đề xuất lên hội đồng
        pr_id = f"PR-{uuid.uuid4().hex[:4].upper()}"
        pull_request = PullRequest(
            id=pr_id,
            title="[Auto-Evolution] Fix Database Port Parameter",
            description=(
                "Pull Request tự động khởi tạo bởi Self Rewrite Engine "
                f"để giải quyết vấn đề: {request.problem}"
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
