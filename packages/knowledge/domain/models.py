from datetime import UTC, datetime  # <-- Thêm timezone vào đây

from pydantic import BaseModel, ConfigDict, Field


class KnowledgeArtifact(BaseModel):
    """Domain Entity đại diện cho một hiện vật tri thức trong hệ thống."""

    id: str | None = Field(default=None, description="Định danh duy nhất")
    title: str = Field(..., description="Tiêu đề của tri thức")
    content: str = Field(..., description="Nội dung tri thức")
    author: str = Field(..., description="Tác giả khởi tạo")
    created_at: datetime = Field(default_factory=lambda: datetime.now(UTC))

    model_config = ConfigDict(frozen=True)  # Entity là bất biến (Immutable)