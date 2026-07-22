from datetime import UTC, datetime

from pydantic import BaseModel, ConfigDict, Field


class Transition(BaseModel):
    trigger: str = Field(..., description="Sự kiện kích hoạt")
    target: str = Field(..., description="Trạng thái đích")

    model_config = ConfigDict(frozen=True)


class State(BaseModel):
    name: str = Field(..., description="Tên trạng thái")
    transitions: list[Transition] = Field(default_factory=list)

    model_config = ConfigDict(frozen=True)


class WorkflowDefinition(BaseModel):
    id: str = Field(..., description="Mã quy trình")
    name: str = Field(..., description="Tên quy trình")
    initial_state: str = Field(..., description="Trạng thái khởi đầu")
    states: list[State] = Field(default_factory=list)

    model_config = ConfigDict(frozen=True)


class WorkflowInstance(BaseModel):
    instance_id: str = Field(..., description="Mã phiên chạy")
    workflow_id: str = Field(..., description="Mã quy trình liên kết")
    current_state: str = Field(..., description="Trạng thái hiện hành")
    history: list[str] = Field(default_factory=list)
    updated_at: datetime = Field(default_factory=lambda: datetime.now(UTC))

    model_config = ConfigDict(frozen=True)
