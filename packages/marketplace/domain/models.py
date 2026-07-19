from datetime import UTC, datetime

from pydantic import BaseModel, ConfigDict, Field


class MarketplaceAsset(BaseModel):
    """Aggregate Root đại diện cho một gói Năng lực đóng gói đăng bán."""

    asset_id: str = Field(..., description="Mã ứng dụng")
    name: str = Field(..., description="Tên ứng dụng")
    category: str = Field(..., description="Phân loại: CAPABILITY, WORKFLOW")
    version: str = Field(default="1.0.0", description="Phiên bản ngữ nghĩa")
    dependencies: list[str] = Field(
        default_factory=list, description="Mã các Năng lực phụ thuộc"
    )
    compatibility_matrix: list[str] = Field(
        default_factory=list, description="Danh sách phiên bản EAOS được hỗ trợ"
    )
    pricing: float = Field(default=0.0, description="Giá dịch vụ tính theo Token")
    license_type: str = Field(default="MIT", description="Mẫu Giấy phép")
    publisher_id: str = Field(..., description="Mã doanh nghiệp phát hành")
    rating: float = Field(default=5.0, description="Điểm số đánh giá từ liên bang")
    manifest_payload: dict[str, str] = Field(..., description="Mô tả cấu trúc")
    published_at: datetime = Field(default_factory=lambda: datetime.now(UTC))

    model_config = ConfigDict(frozen=True)
