import uuid
from datetime import UTC, datetime, timedelta

from pydantic import BaseModel

from packages.prediction.domain.models import Forecast, Prediction, Risk, Trend
from packages.prediction.domain.ports import PredictionRepository


class MetricDatapoint(BaseModel):
    """Äiá»ƒm dá»¯ liá»‡u Ä‘o lÆ°á»ng theo thá»i gian."""

    timestamp: datetime
    value: float


class HistoricalMetricsPayload(BaseModel):
    """Dá»¯ liá»‡u chuá»—i thá»i gian lá»‹ch sá»­ truyá»n vÃ o Ä‘á»ƒ dá»± bÃ¡o."""

    metric_name: str
    datapoints: list[MetricDatapoint]


class RunPredictionUseCase:
    """Application Service phÃ¢n tÃ­ch xu hÆ°á»›ng lá»‹ch sá»­ vÃ  ngoáº¡i suy rá»§i ro."""

    def __init__(self, repo: PredictionRepository) -> None:
        self.repo = repo

    def execute(self, payload: HistoricalMetricsPayload) -> Prediction:
        pred_id = f"PRD-{uuid.uuid4().hex[:6].upper()}"
        datapoints = sorted(payload.datapoints, key=lambda x: x.timestamp)

        if len(datapoints) < 2:
            raise ValueError("Cáº§n tá»‘i thiá»ƒu 2 Ä‘iá»ƒm dá»¯ liá»‡u lá»‹ch sá»­ Ä‘á»ƒ dá»± bÃ¡o.")

        # Thuáº­t toÃ¡n tÃ­nh toÃ¡n Ä‘á»™ dá»‘c xu hÆ°á»›ng
        first_val = datapoints[0].value
        last_val = datapoints[-1].value
        diff = last_val - first_val

        avg_val = sum(d.value for d in datapoints) / len(datapoints)
        is_latency = "latency" in payload.metric_name.lower()

        # XÃ¡c Ä‘á»‹nh hÆ°á»›ng dá»‹ch chuyá»ƒn chá»‰ sá»‘
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

        # Náº¿u phÃ¡t hiá»‡n chá»‰ sá»‘ cÃ³ xu hÆ°á»›ng suy thoÃ¡i
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
                    title=(f"Nguy cÆ¡ sá»¥t giáº£m cháº¥t lÆ°á»£ng chá»‰ sá»‘ {payload.metric_name}"),
                    probability=0.85,
                    timeframe_days=90,
                    severity="HIGH" if is_latency else "MEDIUM",
                )
            )
        else:
            # Náº¿u chá»‰ sá»‘ an toÃ n á»•n Ä‘á»‹nh
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
