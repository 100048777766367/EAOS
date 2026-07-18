from datetime import UTC, datetime

from pydantic import BaseModel, ConfigDict, Field


class AgentExecution(BaseModel):
    """Chi tiết nhật ký thực thi của từng AI Agent trong chuỗi tác vụ."""

    agent_role: str  # Planner, Architect, Coder, Reviewer, Tester
    input_received: str
    output_generated: str
    duration_ms: float

    model_config = ConfigDict(frozen=True)


class Patch(BaseModel):
    """Mô tả nội dung tệp tin Patch dạng unified diff."""

    file_path: str
    diff_content: str

    model_config = ConfigDict(frozen=True)


class PullRequest(BaseModel):
    """Siêu dữ liệu đại diện cho một PR đề xuất thay đổi mã nguồn."""

    id: str
    title: str
    description: str
    source_branch: str
    target_branch: str
    patches: list[Patch] = Field(default_factory=list)

    model_config = ConfigDict(frozen=True)


class SelfRewriteJob(BaseModel):
    """Thực thể điều hành toàn bộ phiên tự lập trình của AI."""

    id: str
    problem: str
    status: str  # "SUCCESS" hoặc "FAILED"
    agent_logs: list[AgentExecution] = Field(default_factory=list)
    pull_request: PullRequest | None = Field(default=None)
    created_at: datetime = Field(default_factory=lambda: datetime.now(UTC))

    model_config = ConfigDict(frozen=True)