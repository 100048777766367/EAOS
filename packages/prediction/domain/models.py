from datetime import UTC, datetime

from pydantic import BaseModel, ConfigDict, Field


class Forecast(BaseModel):
    """Dự báo định lượng về giá trị chỉ số trong tương lai."""

    target_metric: str
    predicted_value: float
    target_date: datetime
    confidence_interval: float  # Độ tự tin từ 0.0 đến 1.0

    model_config = ConfigDict(frozen=True)


class Risk(BaseModel):
    """Rủi ro kiến trúc hoặc vận hành phát hiện được từ dự báo."""

    id: str
    title: str
    probability: float  # Xác suất từ 0.0 đến 1.0
    timeframe_days: int
    severity: str  # HIGH, MEDIUM, LOW

    model_config = ConfigDict(frozen=True)


class Trend(BaseModel):
    """Phân tích xu hướng dựa trên lịch sử đo lường."""

    metric_name: str
    historical_average: float
    direction: str  # "IMPROVING", "STABLE", "DEGRADING"
    slope: float  # Hệ số góc của đường xu hướng

    model_config = ConfigDict(frozen=True)


class Prediction(BaseModel):
    """Thực thể Dự đoán chẩn đoán sớm của hệ điều hành EAOS."""

    id: str
    created_at: datetime = Field(default_factory=lambda: datetime.now(UTC))
    trends: list[Trend] = Field(default_factory=list)
    forecasts: list[Forecast] = Field(default_factory=list)
    risks: list[Risk] = Field(default_factory=list)

    model_config = ConfigDict(frozen=True)
