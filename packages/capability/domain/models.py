from pydantic import BaseModel, ConfigDict, Field


class CapabilityMetadata(BaseModel):
    """Value Object quản lý vòng đời và chủ sở hữu của Năng lực."""

    owner: str = Field(..., description="Chủ thể sở hữu kiểm duyệt")
    status: str = Field(default="active", description="Trạng thái vòng đời")
    description: str = Field(..., description="Mô tả năng lực kinh doanh")

    model_config = ConfigDict(frozen=True)


class CapabilityContract(BaseModel):
    """Mẫu liên kết giao diện API tĩnh (OpenAPI/gRPC)."""

    id: str
    type: str  # "REST", "gRPC", "Event"
    definition_path: str

    model_config = ConfigDict(frozen=True)


class BusinessCapability(BaseModel):
    """Aggregate Root đại diện cho Năng lực thực thi tối cao (Capability)."""

    id: str = Field(..., description="Mã năng lực (ví dụ: capability.identity)")
    name: str = Field(..., description="Tên năng lực nghiệp vụ")
    version: str = Field(..., description="Phiên bản phát hành")
    metadata: CapabilityMetadata
    dependencies: list[str] = Field(default_factory=list)
    policies: list[str] = Field(default_factory=list)
    contracts: list[CapabilityContract] = Field(default_factory=list)
    events: list[str] = Field(default_factory=list)

    model_config = ConfigDict(frozen=True)
