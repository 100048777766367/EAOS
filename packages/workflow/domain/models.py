from datetime import UTC, datetime

from pydantic import BaseModel, ConfigDict, Field


class Transition(BaseModel):
    """Mô tả một bước chuyển trạng thái trong máy trạng thái."""

    trigger: str = Field(..., description="Sự kiện kích hoạt")
    target: str = Field(..., description="Trạng thái đích")

    model_config = ConfigDict(frozen=True)


class State(BaseModel):
    """Mô tả một trạng thái trong quy trình nghiệp vụ."""

    name: str = Field(..., description="Tên trạng thái")
    transitions: list[Transition] = Field(
        default_factory=list, description="Danh sách các bước chuyển tiếp"
    )

    model_config = ConfigDict(frozen=True)


class WorkflowDefinition(BaseModel):
    """Định nghĩa quy trình nghiệp vụ (Workflow Blueprint)."""

    id: str = Field(..., description="Mã quy trình")
    name: str = Field(..., description="Tên quy trình")
    initial_state: str = Field(default="drafted")
    states: list[State] = Field(default_factory=list)

    model_config = ConfigDict(frozen=True)


class WorkflowInstance(BaseModel):
    """Một phiên chạy quy trình nghiệp vụ thực tế (Active Instance)."""

    instance_id: str = Field(..., description="Mã phiên chạy duy nhất")
    workflow_id: str = Field(..., description="Mã định danh quy trình gốc")
    current_state: str = Field(
        default="INITIALIZED", description="Trạng thái hiện tại"
    )
    history: list[str] = Field(
        default_factory=list, description="Nhật ký di chuyển trạng thái"
    )
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(UTC)
    )

    # Cho phép đột biến trạng thái đối tượng khi thực thi use case
    model_config = ConfigDict(arbitrary_types_allowed=True)

    def transition(self, new_state: str) -> None:
        """Cập nhật trạng thái mới có lưu vết lịch sử di chuyển."""
        self.history.append(new_state)
        self.current_state = new_state