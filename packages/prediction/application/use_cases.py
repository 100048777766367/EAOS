import uuid
from datetime import UTC, datetime, timedelta

from pydantic import BaseModel

from packages.prediction.domain.models import Forecast, Prediction, Risk, Trend
from packages.prediction.domain.ports import PredictionRepository


class MetricDatapoint(BaseModel):
    """Điểm dữ liệu đo lường theo thời gian."""

    timestamp: datetime
    value: float


class HistoricalMetricsPayload(BaseModel):
    """Dữ liệu chuỗi thời gian lịch sử truyền vào để dự báo."""

    metric_name: str
    datapoints: list[MetricDatapoint]


class RunPredictionUseCase:
    """Application Service phân tích xu hướng lịch sử và ngoại suy rủi ro."""

    def __init__(self, repo: PredictionRepository) -> None:
        self.repo = repo

    def execute(self, payload: HistoricalMetricsPayload) -> Prediction:
        pred_id = f"PRD-{uuid.uuid4().hex[:6].upper()}"
        datapoints = sorted(payload.datapoints, key=lambda x: x.timestamp)

        if len(datapoints) < 2:
            raise ValueError("Cần tối thiểu 2 điểm dữ liệu lịch sử để dự báo.")

        # Thuật toán tính toán độ dốc xu hướng
        first_val = datapoints[0].value
        last_val = datapoints[-1].value
        diff = last_val - first_val

        avg_val = sum(d.value for d in datapoints) / len(datapoints)
        is_latency = "latency" in payload.metric_name.lower()

        # Xác định hướng dịch chuyển chỉ số
        if diff == 0:
            direction = "STABLE"
        elif (diff > 0 and is_latency) or (diff < 0 and not is_latency):
            direction = "DEGRADING"
        else:
            direction = "IMPROVING"

        trends = [
            Trend(
                metric_name=payload.metric_name,
                historical_average=round(avg_val, 2),
                direction=direction,
                slope=round(diff, 4),
            )
        ]

        forecasts = []
        risks = []

        # Nếu phát hiện chỉ số có xu hướng suy thoái
        if direction == "DEGRADING":
            projected_value = last_val + (diff * 3)
            target_date = datetime.now(UTC) + timedelta(days=90)

            forecasts.append(
                Forecast(
                    target_metric=payload.metric_name,
                    predicted_value=round(projected_value, 2),
                    target_date=target_date,
                    confidence_interval=0.85,
                )
            )

            risks.append(
                Risk(
                    id="RSK-01",
                    title=(f"Nguy cơ sụt giảm chất lượng chỉ số {payload.metric_name}"),
                    probability=0.85,
                    timeframe_days=90,
                    severity="HIGH" if is_latency else "MEDIUM",
                )
            )
        else:
            # Nếu chỉ số an toàn ổn định
            target_date = datetime.now(UTC) + timedelta(days=90)
            forecasts.append(
                Forecast(
                    target_metric=payload.metric_name,
                    predicted_value=round(last_val, 2),
                    target_date=target_date,
                    confidence_interval=0.90,
                )
            )

        prediction = Prediction(
            id=pred_id,
            created_at=datetime.now(UTC),
            trends=trends,
            forecasts=forecasts,
            risks=risks,
        )

        return self.repo.save(prediction)
