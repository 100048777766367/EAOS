from packages.knowledge.domain.models import KnowledgeArtifact
from packages.knowledge.domain.ports import KnowledgeRepository
from sqlalchemy import Column, DateTime, String, Text, create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

Base = declarative_base()


class PostgresKnowledgeModel(Base):
    """SQLAlchemy model để ánh xạ xuống cơ sở dữ liệu."""

    __tablename__ = "knowledge_artifacts"

    id = Column(String, primary_key=True)
    title = Column(String, nullable=False)
    content = Column(Text, nullable=False)
    author = Column(String, nullable=False)
    created_at = Column(DateTime, nullable=False)


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