from datetime import UTC, datetime

from pydantic import BaseModel, ConfigDict, Field


class Forecast(BaseModel):
    """Dá»± bÃ¡o Ä‘á»‹nh lÆ°á»£ng vá» giÃ¡ trá»‹ chá»‰ sá»‘ trong tÆ°Æ¡ng lai."""

    target_metric: str
    predicted_value: float
    target_date: datetime
    confidence_interval: float  # Äá»™ tá»± tin tá»« 0.0 Ä‘áº¿n 1.0

    model_config = ConfigDict(frozen=True)


class Risk(BaseModel):
    """Rá»§i ro kiáº¿n trÃºc hoáº·c váº­n hÃ nh phÃ¡t hiá»‡n Ä‘Æ°á»£c tá»« dá»± bÃ¡o."""

    id: str
    title: str
    probability: float  # XÃ¡c suáº¥t tá»« 0.0 Ä‘áº¿n 1.0
    timeframe_days: int
    severity: str  # HIGH, MEDIUM, LOW

    model_config = ConfigDict(frozen=True)


class Trend(BaseModel):
    """PhÃ¢n tÃ­ch xu hÆ°á»›ng dá»±a trÃªn lá»‹ch sá»­ Ä‘o lÆ°á»ng."""

    metric_name: str
    historical_average: float
    direction: str  # "IMPROVING", "STABLE", "DEGRADING"
    slope: float  # Há»‡ sá»‘ gÃ³c cá»§a Ä‘Æ°á»ng xu hÆ°á»›ng

    model_config = ConfigDict(frozen=True)


class Prediction(BaseModel):
    """Thá»±c thá»ƒ Dá»± Ä‘oÃ¡n cháº©n Ä‘oÃ¡n sá»›m cá»§a há»‡ Ä‘iá»u hÃ nh EAOS."""

    id: str
    created_at: datetime = Field(default_factory=lambda: datetime.now(UTC))
    trends: list[Trend] = Field(default_factory=list)
    forecasts: list[Forecast] = Field(default_factory=list)
    risks: list[Risk] = Field(default_factory=list)

    model_config = ConfigDict(frozen=True)
