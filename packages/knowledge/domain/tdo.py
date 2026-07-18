import hashlib
from datetime import UTC, datetime

from pydantic import BaseModel, Field

from packages.knowledge.domain.models import KnowledgeArtifact


class TDOFixity(BaseModel):
    """Mã Hash bảo đảm tính toàn vẹn (Fixity Proof) chống sửa đổi tệp."""

    algorithm: str = "SHA-256"
    value: str


class TDOPromptProvenance(BaseModel):
    """Nguồn gốc lịch sử khởi tạo tài liệu chuẩn bởi Con người hay AI."""

    author: str
    timestamp: datetime = Field(default_factory=lambda: datetime.now(UTC))
    system_version: str = "0.1.0"


class TrustworthyDigitalObject(BaseModel):
    """Đối tượng số đáng tin cậy tự mô tả chính nó (Self-describing TDO)."""

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
    """Đóng gói dữ liệu tri thức thô thành TDO tự mô tả chuẩn mực."""
    # Tạo mã định danh ngữ nghĩa duy nhất
    raw_payload = f"{artifact.title}|{artifact.content}|{artifact.author}"
    sha256_hash = hashlib.sha256(raw_payload.encode("utf-8")).hexdigest()

    provenance = TDOPromptProvenance(author=author)
    fixity = TDOFixity(value=sha256_hash)

    return TrustworthyDigitalObject(
        metadata=provenance,
        data=artifact,
        fixity=fixity,
    )