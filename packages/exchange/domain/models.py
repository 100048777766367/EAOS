from datetime import UTC, datetime

from pydantic import BaseModel, ConfigDict, Field


class LinkedGraphNode(BaseModel):
    """SÆ¡ Ä‘á»“ nÃºt liÃªn káº¿t ngá»¯ nghÄ©a liÃªn doanh nghiá»‡p báº±ng RDF (Sprint 3)."""

    uri: str = Field(..., description="Äá»‹a chá»‰ URI Ä‘á»‹nh danh ngá»¯ nghÄ©a toÃ n cáº§u")
    relation: str = Field(..., description="Quan há»‡: hasSharedPolicy, trustMember")
    target_uri: str = Field(..., description="Äá»‹a chá»‰ URI cá»§a nÃºt Ä‘Ã­ch")

    model_config = ConfigDict(frozen=True)


class SharedEcosystemEvent(BaseModel):
    """Sá»± kiá»‡n phi Ä‘á»“ng bá»™ truyá»n phÃ¡t xuyÃªn tá»• chá»©c trÃªn Event Mesh (Sprint 4)."""

    event_id: str
    sender_tenant_id: str
    event_type: str  # "PolicyUpdated", "CapabilityPublished"
    payload: dict[str, str]
    timestamp: datetime = Field(default_factory=lambda: datetime.now(UTC))

    model_config = ConfigDict(frozen=True)
