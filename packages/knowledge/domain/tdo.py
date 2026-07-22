import hashlib
from datetime import UTC, datetime

from pydantic import BaseModel, Field

from packages.knowledge.domain.models import KnowledgeArtifact


class TDOFixity(BaseModel):
    """MÃ£ Hash báº£o Ä‘áº£m tÃ­nh toÃ n váº¹n (Fixity Proof) chá»‘ng sá»­a Ä‘á»•i tá»‡p."""

    algorithm: str = "SHA-256"
    value: str


class TDOPromptProvenance(BaseModel):
    """Nguá»“n gá»‘c lá»‹ch sá»­ khá»Ÿi táº¡o tÃ i liá»‡u chuáº©n bá»Ÿi Con ngÆ°á»i hay AI."""

    author: str
    timestamp: datetime = Field(default_factory=lambda: datetime.now(UTC))
    system_version: str = "0.1.0"


class TrustworthyDigitalObject(BaseModel):
    """Äá»‘i tÆ°á»£ng sá»‘ Ä‘Ã¡ng tin cáº­y tá»± mÃ´ táº£ chÃ­nh nÃ³ (Self-describing TDO)."""

    context: str = Field(
        default="https://eaos.internal/contexts/governance.jsonld",
        alias="@context",
    )
    doc_type: str = Field(default="ArchitectureArtifact", alias="@type")
    metadata: TDOPromptProvenance
    data: KnowledgeArtifact
    fixity: TDOFixity

    model_config = {"populate_by_name": True}


def encapsulate_artifact(
    artifact: KnowledgeArtifact, author: str
) -> TrustworthyDigitalObject:
    """ÄÃ³ng gÃ³i dá»¯ liá»‡u tri thá»©c thÃ´ thÃ nh TDO tá»± mÃ´ táº£ chuáº©n má»±c."""
    # Táº¡o mÃ£ Ä‘á»‹nh danh ngá»¯ nghÄ©a duy nháº¥t
    raw_payload = f"{artifact.title}|{artifact.content}|{artifact.author}"
    sha256_hash = hashlib.sha256(raw_payload.encode("utf-8")).hexdigest()

    provenance = TDOPromptProvenance(author=author)
    fixity = TDOFixity(value=sha256_hash)

    return TrustworthyDigitalObject(
        metadata=provenance,
        data=artifact,
        fixity=fixity,
    )

