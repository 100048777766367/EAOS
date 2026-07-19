from pydantic import BaseModel, ConfigDict, Field


class AgentConfig(BaseModel):
    """Value Object quản lý cấu hình và tham số mô hình LLM của Agent."""

    model_name: str = Field(..., description="Tên mô hình LLM sử dụng")
    temperature: float = Field(default=0.2, description="Độ sáng tạo")
    max_tokens: int = Field(default=4096, description="Giới hạn token")

    model_config = ConfigDict(frozen=True)


class AIAgent(BaseModel):
    """Aggregate Root đại diện cho một AI Agent thực thi có Lifecycle."""

    id: str = Field(..., description="Mã Agent duy nhất (agent.planner)")
    role: str = Field(..., description="Vai trò đảm nhiệm (Planner, Coder)")
    config: AgentConfig
    current_state: str = Field(default="INITIALIZED")
    lifecycle_history: list[str] = Field(default_factory=list)

    model_config = ConfigDict(frozen=True)