from datetime import UTC, datetime

from pydantic import BaseModel, ConfigDict, Field


class MarketplaceAsset(BaseModel):
    """Aggregate Root Ä‘áº¡i diá»‡n cho má»™t gÃ³i NÄƒng lá»±c Ä‘Ã³ng gÃ³i Ä‘Äƒng bÃ¡n."""

    asset_id: str = Field(..., description="MÃ£ á»©ng dá»¥ng")
    name: str = Field(..., description="TÃªn á»©ng dá»¥ng")
    category: str = Field(..., description="PhÃ¢n loáº¡i: CAPABILITY, WORKFLOW")
    version: str = Field(default="1.0.0", description="PhiÃªn báº£n ngá»¯ nghÄ©a")
    dependencies: list[str] = Field(
        default_factory=list, description="MÃ£ cÃ¡c NÄƒng lá»±c phá»¥ thuá»™c"
    )
    compatibility_matrix: list[str] = Field(
        default_factory=list, description="Danh sÃ¡ch phiÃªn báº£n EAOS Ä‘Æ°á»£c há»— trá»£"
    )
    pricing: float = Field(default=0.0, description="GiÃ¡ dá»‹ch vá»¥ tÃ­nh theo Token")
    license_type: str = Field(default="MIT", description="Máº«u Giáº¥y phÃ©p")
    publisher_id: str = Field(..., description="MÃ£ doanh nghiá»‡p phÃ¡t hÃ nh")
    rating: float = Field(default=5.0, description="Äiá»ƒm sá»‘ Ä‘Ã¡nh giÃ¡ tá»« liÃªn bang")
    manifest_payload: dict[str, str] = Field(..., description="MÃ´ táº£ cáº¥u trÃºc")
    published_at: datetime = Field(default_factory=lambda: datetime.now(UTC))

    model_config = ConfigDict(frozen=True)

