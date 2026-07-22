from datetime import UTC, datetime

from pydantic import BaseModel, ConfigDict, Field


class RootCause(BaseModel):
    """MÃ´ táº£ chi tiáº¿t nguyÃªn nhÃ¢n gá»‘c rá»… gÃ¢y ra sá»¥t giáº£m chá»‰ sá»‘ thá»ƒ lá»±c."""

    id: str = Field(..., description="MÃ£ nguyÃªn nhÃ¢n")
    type: str = Field(..., description="PhÃ¢n loáº¡i nguyÃªn nhÃ¢n lá»—i")
    description: str = Field(..., description="MÃ´ táº£ chi tiáº¿t sá»± cá»‘")
    probability: float = Field(..., description="XÃ¡c suáº¥t chÃ­nh xÃ¡c (0.0-1.0)")
    evidence: list[str] = Field(default_factory=list, description="Báº±ng chá»©ng")

    model_config = ConfigDict(frozen=True)


class Recommendation(BaseModel):
    """Khuyáº¿n nghá»‹ hÃ nh Ä‘á»™ng kháº¯c phá»¥c lá»—i Ä‘Æ°á»£c Ä‘á» xuáº¥t bá»Ÿi Reflection."""

    priority: str = Field(..., description="Má»©c Ä‘á»™ Æ°u tiÃªn (HIGH/MEDIUM/LOW)")
    action: str = Field(..., description="HÃ nh Ä‘á»™ng sá»­a Ä‘á»•i cáº§n thá»±c hiá»‡n")
    reason: str = Field(..., description="LÃ½ do Ä‘á» xuáº¥t")
    risk: str = Field(..., description="Rá»§i ro Ä‘i kÃ¨m khi thá»±c thi")

    model_config = ConfigDict(frozen=True)


class ReflectionReport(BaseModel):
    """BÃ¡o cÃ¡o tá»± suy ngáº«m vÃ  cháº©n Ä‘oÃ¡n sá»± cá»‘ hoÃ n chá»‰nh cá»§a EAOS."""

    id: str = Field(..., description="MÃ£ bÃ¡o cÃ¡o duy nháº¥t")
    subject: str = Field(..., description="MÃ£ Ä‘á»‘i tÆ°á»£ng kiá»ƒm tra (artifact_id)")
    trigger: str = Field(..., description="Sá»± kiá»‡n kÃ­ch hoáº¡t (Fitness Fail)")
    root_causes: list[RootCause] = Field(default_factory=list)
    confidence: float = Field(..., description="Äá»™ tá»± tin cá»§a bÃ¡o cÃ¡o")
    recommendations: list[Recommendation] = Field(default_factory=list)
    created_at: datetime = Field(default_factory=lambda: datetime.now(UTC))

    model_config = ConfigDict(frozen=True)

