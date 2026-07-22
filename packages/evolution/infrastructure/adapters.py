from datetime import datetime
from typing import Any

from sqlalchemy import String, create_engine
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, sessionmaker
from sqlalchemy.types import JSON

from packages.evolution.domain.models import (
    Evidence,
    EvolutionObject,
    Metadata,
    Provenance,
)
from packages.evolution.domain.ports import EvolutionRepository


class Base(DeclarativeBase):
    pass


class PostgresEvolutionModel(Base):
    __tablename__ = "evolution_objects"

    id: Mapped[str] = mapped_column(String, primary_key=True)
    name: Mapped[str] = mapped_column(String, nullable=False)
    payload: Mapped[dict[str, Any]] = mapped_column(JSON, nullable=False)
    metadata_json: Mapped[dict[str, Any]] = mapped_column(JSON, nullable=False)
    provenance_json: Mapped[dict[str, Any]] = mapped_column(JSON, nullable=False)
    evidences_json: Mapped[list[dict[str, Any]]] = mapped_column(JSON, nullable=False)
    version: Mapped[int] = mapped_column(nullable=False, default=1)
    parent_id: Mapped[str | None] = mapped_column(String, nullable=True)


class PostgresEvolutionRepository(EvolutionRepository):
    """Adapter hiện thực hóa Port kết nối PostgreSQL cho tiến hóa kiến trúc."""

    def __init__(self, db_url: str) -> None:
        self.engine = create_engine(db_url)
        Base.metadata.create_all(self.engine)
        self.SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)

    def save(self, obj: EvolutionObject) -> EvolutionObject:
        db_session = self.SessionLocal()

        metadata_dict = obj.metadata.model_dump()
        provenance_dict = obj.provenance.model_dump()
        provenance_dict["timestamp"] = obj.provenance.timestamp.isoformat()

        evidences_list = []
        for ev in obj.evidences:
            ev_dict = ev.model_dump()
            ev_dict["verified_at"] = ev.verified_at.isoformat()
            evidences_list.append(ev_dict)

        parent_id = obj.provenance.parent_id
        version = obj.payload.get("__version", 1)

        db_model = PostgresEvolutionModel(
            id=obj.id,
            name=obj.name,
            payload=obj.payload,
            metadata_json=metadata_dict,
            provenance_json=provenance_dict,
            evidences_json=evidences_list,
            version=version,
            parent_id=parent_id,
        )
        try:
            db_session.merge(db_model)
            db_session.commit()
            return obj
        finally:
            db_session.close()

    def find_by_id(self, obj_id: str) -> EvolutionObject | None:
        db_session = self.SessionLocal()
        try:
            db_model = db_session.query(PostgresEvolutionModel).filter(PostgresEvolutionModel.id == obj_id).first()
            if not db_model:
                return None

            meta_data = Metadata(**db_model.metadata_json)
            prov_data = db_model.provenance_json
            prov_data["timestamp"] = datetime.fromisoformat(prov_data["timestamp"])
            provenance = Provenance(**prov_data)

            evidences = []
            for ev_data in db_model.evidences_json:
                ev_data["verified_at"] = datetime.fromisoformat(ev_data["verified_at"])
                evidences.append(Evidence(**ev_data))

            return EvolutionObject(
                id=db_model.id,
                name=db_model.name,
                payload=db_model.payload,
                metadata=meta_data,
                provenance=provenance,
                evidences=evidences,
            )
        finally:
            db_session.close()

    def get_lineage(self, start_id: str) -> list[str]:
        """Truy vết chuỗi gia phả (lineage tree) đi ngược về nút gốc."""
        db_session = self.SessionLocal()
        lineage = []
        curr_id: str | None = start_id
        try:
            while curr_id:
                db_model = db_session.query(PostgresEvolutionModel).filter(PostgresEvolutionModel.id == curr_id).first()
                if not db_model:
                    break
                lineage.append(curr_id)
                curr_id = db_model.parent_id
            return lineage
        finally:
            db_session.close()

    def find_snapshot_by_id(self, snapshot_id: str) -> Any | None:
        return None

    def save_snapshot(self, snapshot: Any) -> Any:
        return snapshot


class InMemoryEvolutionRepository(EvolutionRepository):
    """Bộ lưu trữ tiến hóa tạm thời trong bộ nhớ đệm RAM phục vụ testing."""

    def __init__(self) -> None:
        self._store: dict[str, EvolutionObject] = {}

    def save(self, obj: EvolutionObject) -> EvolutionObject:
        self._store[obj.id] = obj
        return obj

    def find_by_id(self, obj_id: str) -> EvolutionObject | None:
        return self._store.get(obj_id)

    def get_lineage(self, start_id: str) -> list[str]:
        lineage = []
        curr_id: str | None = start_id
        while curr_id:
            obj = self.find_by_id(curr_id)
            if not obj:
                break
            lineage.append(curr_id)
            curr_id = obj.provenance.parent_id
        return lineage

    def find_snapshot_by_id(self, snapshot_id: str) -> Any | None:
        return None

    def save_snapshot(self, snapshot: Any) -> Any:
        return snapshot
