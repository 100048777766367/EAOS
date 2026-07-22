import hashlib
from datetime import UTC, datetime
from typing import Any

from pydantic import BaseModel, ConfigDict, Field


class Entity(BaseModel):
    id: str


class AggregateRoot(Entity):
    pass


class ValueObject(BaseModel):
    model_config = ConfigDict(frozen=True)


class TDOFixity(BaseModel):
    algorithm: str = "SHA-256"
    value: str

    model_config = ConfigDict(frozen=True)


class TDOPromptProvenance(BaseModel):
    author: str
    timestamp: datetime = Field(default_factory=lambda: datetime.now(UTC))
    system_version: str = "0.1.0"

    model_config = ConfigDict(frozen=True)


class TrustworthyDigitalObject(BaseModel):
    """Đối tượng số đáng tin cậy tự mô tả (Self-describing TDO) [1.1.4]."""

    context: str = Field(
        default="https://eaos.internal/contexts/governance.jsonld",
        alias="@context",
    )
    doc_type: str = Field(default="ArchitectureArtifact", alias="@type")
    metadata: TDOPromptProvenance
    data: Any
    fixity: TDOFixity

    model_config = ConfigDict(populate_by_name=True)


def encapsulate_artifact(
    artifact_id: str, title: str, content: str, author: str
) -> TrustworthyDigitalObject:
    """Đóng gói dữ liệu tri thức thô thành TDO tự mô tả [1.1.4]."""
    raw_payload = f"{title}|{content}|{author}"
    sha256_hash = hashlib.sha256(raw_payload.encode("utf-8")).hexdigest()

    provenance = TDOPromptProvenance(author=author)
    fixity = TDOFixity(value=sha256_hash)

    data_payload = {"id": artifact_id, "title": title, "content": content}

    return TrustworthyDigitalObject(
        metadata=provenance,
        data=data_payload,
        fixity=fixity,
    )
