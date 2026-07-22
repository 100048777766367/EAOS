"""Infrastructure adapters for Architecture Memory context."""

from datetime import datetime

from packages.architecture_memory.domain.models import (
    ArchitectureMemoryRecordAggregate,
    MemoryTier,
    MemoryType,
)
from packages.architecture_memory.domain.ports import (
    ArchitectureMemoryRepositoryPort,
    SemanticRecallPort,
)
from sqlalchemy import DateTime, Float, String, Text, create_engine, select
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, sessionmaker


class InMemoryArchitectureMemoryRepository(
    ArchitectureMemoryRepositoryPort, SemanticRecallPort
):
    def __init__(self) -> None:
        self._store: dict[str, ArchitectureMemoryRecordAggregate] = {}

    def save(self, record: ArchitectureMemoryRecordAggregate) -> None:
        self._store[record.memory_id] = record

    def find_by_id(
        self, memory_id: str
    ) -> ArchitectureMemoryRecordAggregate | None:
        return self._store.get(memory_id)

    def list_all(self) -> list[ArchitectureMemoryRecordAggregate]:
        return list(self._store.values())

    def recall_relevant_memories(
        self, query_text: str, limit: int = 5, min_similarity: float = 0.1
    ) -> list[tuple[ArchitectureMemoryRecordAggregate, float]]:
        query_tokens = set(query_text.lower().split())
        scored_records: list[
            tuple[ArchitectureMemoryRecordAggregate, float]
        ] = []

        for record in self._store.values():
            sim = record.calculate_similarity(query_tokens)
            if sim >= min_similarity:
                scored_records.append((record, sim))

        scored_records.sort(key=lambda x: x[1], reverse=True)
        return scored_records[:limit]


class Base(DeclarativeBase):
    pass


class PgMemoryRecordModel(Base):
    __tablename__ = "architecture_memory_records"

    id: Mapped[str] = mapped_column(String, primary_key=True)
    tier: Mapped[str] = mapped_column(String, nullable=False)
    memory_type: Mapped[str] = mapped_column(String, nullable=False)
    title: Mapped[str] = mapped_column(String, nullable=False)
    context_summary: Mapped[Text] = mapped_column(Text, nullable=False)
    lesson_learned: Mapped[Text] = mapped_column(Text, nullable=False)
    linked_adr_id: Mapped[str | None] = mapped_column(String, nullable=True)
    confidence_score: Mapped[float] = mapped_column(Float, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, nullable=False)


class PgVectorArchitectureMemoryAdapter(
    ArchitectureMemoryRepositoryPort, SemanticRecallPort
):
    """pgvector implementation of Architecture Memory persistence."""

    def __init__(self, db_url: str) -> None:
        self.engine = create_engine(db_url)
        Base.metadata.create_all(self.engine)
        self.SessionLocal = sessionmaker(
            autocommit=False, autoflush=False, bind=self.engine
        )

    def save(self, record: ArchitectureMemoryRecordAggregate) -> None:
        session = self.SessionLocal()
        try:
            model = PgMemoryRecordModel(
                id=record.memory_id,
                tier=record.tier.name,
                memory_type=record.memory_type.name,
                title=record.title,
                context_summary=record.context_summary,
                lesson_learned=record.lesson_learned,
                linked_adr_id=record.linked_adr_id,
                confidence_score=record.confidence_score,
                created_at=record.created_at,
            )
            session.merge(model)
            session.commit()
        finally:
            session.close()

    def find_by_id(
        self, memory_id: str
    ) -> ArchitectureMemoryRecordAggregate | None:
        session = self.SessionLocal()
        try:
            stmt = select(PgMemoryRecordModel).where(
                PgMemoryRecordModel.id == memory_id
            )
            model = session.scalar(stmt)
            if not model:
                return None

            return ArchitectureMemoryRecordAggregate(
                memory_id=model.id,
                tier=MemoryTier[model.tier],
                memory_type=MemoryType[model.memory_type],
                title=model.title,
                context_summary=str(model.context_summary),
                lesson_learned=str(model.lesson_learned),
                linked_adr_id=model.linked_adr_id,
                confidence_score=model.confidence_score,
                created_at=model.created_at,
            )
        finally:
            session.close()

    def list_all(self) -> list[ArchitectureMemoryRecordAggregate]:
        session = self.SessionLocal()
        try:
            stmt = select(PgMemoryRecordModel)
            models = session.scalars(stmt).all()
            return [
                ArchitectureMemoryRecordAggregate(
                    memory_id=m.id,
                    tier=MemoryTier[m.tier],
                    memory_type=MemoryType[m.memory_type],
                    title=m.title,
                    context_summary=str(m.context_summary),
                    lesson_learned=str(m.lesson_learned),
                    linked_adr_id=m.linked_adr_id,
                    confidence_score=m.confidence_score,
                    created_at=m.created_at,
                )
                for m in models
            ]
        finally:
            session.close()

    def recall_relevant_memories(
        self, query_text: str, limit: int = 5, min_similarity: float = 0.1
    ) -> list[tuple[ArchitectureMemoryRecordAggregate, float]]:
        all_records = self.list_all()
        query_tokens = set(query_text.lower().split())

        scored_records: list[
            tuple[ArchitectureMemoryRecordAggregate, float]
        ] = []
        for record in all_records:
            sim = record.calculate_similarity(query_tokens)
            if sim >= min_similarity:
                scored_records.append((record, sim))

        scored_records.sort(key=lambda x: x[1], reverse=True)
        return scored_records[:limit]
