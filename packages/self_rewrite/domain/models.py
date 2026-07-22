from datetime import UTC, datetime

from pydantic import BaseModel, ConfigDict, Field


class AgentExecution(BaseModel):
    """Chi tiáº¿t nháº­t kÃ½ thá»±c thi cá»§a tá»«ng AI Agent trong chuá»—i tÃ¡c vá»¥."""

    agent_role: str  # Planner, Architect, Coder, Reviewer, Tester
    input_received: str
    output_generated: str
    duration_ms: float

    model_config = ConfigDict(frozen=True)


class Patch(BaseModel):
    """MÃ´ táº£ ná»™i dung tá»‡p tin Patch dáº¡ng unified diff."""

    file_path: str
    diff_content: str

    model_config = ConfigDict(frozen=True)


class PullRequest(BaseModel):
    """SiÃªu dá»¯ liá»‡u Ä‘áº¡i diá»‡n cho má»™t PR Ä‘á» xuáº¥t thay Ä‘á»•i mÃ£ nguá»“n."""

    id: str
    title: str
    description: str
    source_branch: str
    target_branch: str
    patches: list[Patch] = Field(default_factory=list)

    model_config = ConfigDict(frozen=True)


class SelfRewriteJob(BaseModel):
    """Thá»±c thá»ƒ Ä‘iá»u hÃ nh toÃ n bá»™ phiÃªn tá»± láº­p trÃ¬nh cá»§a AI."""

    id: str
    problem: str
    status: str  # "SUCCESS" hoáº·c "FAILED"
    agent_logs: list[AgentExecution] = Field(default_factory=list)
    pull_request: PullRequest | None = Field(default=None)
    created_at: datetime = Field(default_factory=lambda: datetime.now(UTC))

    model_config = ConfigDict(frozen=True)
