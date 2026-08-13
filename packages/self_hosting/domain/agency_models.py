from datetime import UTC, datetime

from pydantic import BaseModel, ConfigDict, Field

"""AI Digital Solopreneur Content Agency Domain Models for EAOS."""


class EndToEndBusinessFlowResult(BaseModel):
    """Value object representing evidence from 12-step execution."""

    model_config = ConfigDict(frozen=True)

    execution_id: str
    keyword_researched: str
    article_slug: str
    lead_captured_email: str
    order_amount_usd: float
    net_profit_usd: float
    ai_cost_usd: float
    roi_percentage: float
    architecture_drift: float
    is_evidence_verified: bool = True
    timestamp: datetime = Field(default_factory=lambda: datetime.now(UTC))
