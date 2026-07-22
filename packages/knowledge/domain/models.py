from datetime import UTC, datetime

from pydantic import BaseModel, ConfigDict, Field


class KnowledgeArtifact(BaseModel):
    """Domain Entity Ä‘áº¡i diá»‡n cho má»™t hiá»‡n váº­t tri thá»©c trong há»‡ thá»‘ng."""

    id: str | None = Field(default=None, description="Äá»‹nh danh duy nháº¥t")
    title: str = Field(..., description="TiÃªu Ä‘á» cá»§a tri thá»©c")
    content: str = Field(..., description="Ná»™i dung tri thá»©c")
    author: str = Field(..., description="TÃ¡c giáº£ khá»Ÿi táº¡o")
    created_at: datetime = Field(default_factory=lambda: datetime.now(UTC))

    model_config = ConfigDict(frozen=True)  # Entity lÃ  báº¥t biáº¿n (Immutable)


class AuditLogEntry(BaseModel):
    """Báº£n ghi lÆ°u láº¡i nháº­t kÃ½ thay Ä‘á»•i phá»¥c vá»¥ lÆ°u váº¿t thÃªm/sá»­a/xÃ³a."""

    action: str  # "ADD", "EDIT", "DELETE"
    timestamp: datetime = Field(default_factory=lambda: datetime.now(UTC))
    author: str
    details: str

