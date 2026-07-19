from datetime import datetime
from typing import Any

from sqlalchemy import DateTime, String, Text, create_engine
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, sessionmaker

from packages.knowledge.domain.models import AuditLogEntry, KnowledgeArtifact
from packages.knowledge.domain.ports import KnowledgeRepository
from packages.knowledge.domain.splay_tree import SplayTree


class Base(DeclarativeBase):
    pass


class PostgresKnowledgeModel(Base):
    __tablename__ = "knowledge_artifacts"

    id: Mapped[str] = mapped_column(String, primary_key=True)
    title: Mapped[str] = mapped_column(String, nullable=False)
    content: Mapped[str] = mapped_column(Text, nullable=False)
    author: Mapped[str] = mapped_column(String, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, nullable=False)


class PostgresKnowledgeRepository(KnowledgeRepository):
    """Adapter hiện thực hóa Port kết nối PostgreSQL."""

    def __init__(self, db_url: str) -> None:
        self.engine = create_engine(db_url)
        Base.metadata.create_all(self.engine)
        self.SessionLocal = sessionmaker(
            autocommit=False, autoflush=False, bind=self.engine
        )

    def save(self, artifact: KnowledgeArtifact) -> KnowledgeArtifact:
        db_session = self.SessionLocal()
        import uuid

        artifact_id = artifact.id or str(uuid.uuid4())

        db_model = PostgresKnowledgeModel(
            id=artifact_id,
            title=artifact.title,
            content=artifact.content,
            author=artifact.author,
            created_at=artifact.created_at,
        )
        try:
            db_session.add(db_model)
            db_session.commit()
            return KnowledgeArtifact(
                id=artifact_id,
                title=artifact.title,
                content=artifact.content,
                author=artifact.author,
                created_at=artifact.created_at,
            )
        finally:
            db_session.close()

    def find_by_id(self, artifact_id: str) -> KnowledgeArtifact | None:
        db_session = self.SessionLocal()
        try:
            db_model = (
                db_session.query(PostgresKnowledgeModel)
                .filter(PostgresKnowledgeModel.id == artifact_id)
                .first()
            )
            if not db_model:
                return None
            return KnowledgeArtifact(
                id=db_model.id,
                title=db_model.title,
                content=db_model.content,
                author=db_model.author,
                created_at=db_model.created_at,
            )
        finally:
            db_session.close()


class SplayCacheKnowledgeRepository(KnowledgeRepository):
    """Decorator bọc ngoài Postgres Repository bằng Splay Tree & Log."""

    def __init__(self, target_repo: KnowledgeRepository) -> None:
        self.target_repo = target_repo
        self.splay_tree: SplayTree[KnowledgeArtifact] = SplayTree()
        # Lưu vết lịch sử thay đổi: id -> list[AuditLogEntry]
        self.audit_history: dict[str, list[AuditLogEntry]] = {}

    def save(self, artifact: KnowledgeArtifact) -> KnowledgeArtifact:
        # Kiểm tra xem tài liệu đã tồn tại chưa
        is_edit = False
        if artifact.id:
            existing = self.target_repo.find_by_id(artifact.id)
            if existing is not None:
                is_edit = True

        # Ghi nhận bền vững xuống Postgres DB
        saved_artifact = self.target_repo.save(artifact)
        artifact_id = saved_artifact.id

        if artifact_id:
            # Chèn vào Splay Tree cache
            self.splay_tree.insert(artifact_id, saved_artifact)

            # Ghi nhận log lịch sử thay đổi
            action_type = "EDIT" if is_edit else "ADD"
            log_entry = AuditLogEntry(
                action=action_type,
                author=saved_artifact.author,
                details=f"Lưu tài liệu: '{saved_artifact.title}'",
            )
            if artifact_id not in self.audit_history:
                self.audit_history[artifact_id] = []
            self.audit_history[artifact_id].append(log_entry)

        return saved_artifact

    def find_by_id(self, artifact_id: str) -> KnowledgeArtifact | None:
        # Tra cứu trên Splay Tree đệm trước
        node = self.splay_tree.search(artifact_id)
        if node is not None:
            return node.value

        # Nếu cache-miss, nạp từ Postgres DB
        artifact = self.target_repo.find_by_id(artifact_id)
        if artifact is not None:
            self.splay_tree.insert(artifact_id, artifact)
        return artifact

    def delete(self, artifact_id: str, author: str) -> bool:
        """Xóa tài liệu khỏi Splay Tree cache."""
        artifact = self.find_by_id(artifact_id)
        if not artifact:
            return False

        deleted = self.splay_tree.delete(artifact_id)
        if deleted:
            log_entry = AuditLogEntry(
                action="DELETE",
                author=author,
                details=f"Đã xóa khỏi Splay Tree: '{artifact.title}'",
            )
            if artifact_id not in self.audit_history:
                self.audit_history[artifact_id] = []
            self.audit_history[artifact_id].append(log_entry)
        return deleted

    def get_tree_layout(self) -> dict[str, Any] | None:
        return self.splay_tree.to_dict()

    def get_tree_mermaid(self) -> str:
        return self.splay_tree.to_mermaid()

    def get_audit_logs(self, artifact_id: str) -> list[AuditLogEntry]:
        return self.audit_history.get(artifact_id, [])
