from datetime import datetime
from typing import Any

from sqlalchemy import DateTime, String, create_engine
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, sessionmaker

from packages.autonomous.domain.models import LoopCycle
from packages.autonomous.domain.ports import AutonomousRepository


class Base(DeclarativeBase):
    pass


class PostgresLoopCycleModel(Base):
    """SQLAlchemy 2.0 Model lưu trữ bền vững trạng thái chu kỳ tiến hóa."""

    __tablename__ = "autonomous_loop_cycles"

    cycle_id: Mapped[str] = mapped_column(String, primary_key=True)
    status: Mapped[str] = mapped_column(String, nullable=False)
    stage_executions_json: Mapped[dict[str, Any]] = mapped_column(
        JSONB, nullable=False
    )
    timestamp: Mapped[datetime] = mapped_column(DateTime, nullable=False)


class PostgresAutonomousRepository(AutonomousRepository):
    """Adapter hiện thực hóa Port kết nối PostgreSQL cho Vòng lặp tự trị."""

    def __init__(self, db_url: str) -> None:
        self.engine = create_engine(db_url)
        Base.metadata.create_all(self.engine)
        self.SessionLocal = sessionmaker(
            autocommit=False, autoflush=False, bind=self.engine
        )

    def save(self, cycle: LoopCycle) -> LoopCycle:
        db_session = self.SessionLocal()
        db_model = PostgresLoopCycleModel(
            cycle_id=cycle.cycle_id,
            status=cycle.status,
            stage_executions_json=cycle.stage_executions,
            timestamp=cycle.timestamp,
        )
        try:
            db_session.merge(db_model)
            db_session.commit()
            return cycle
        finally:
            db_session.close()

    def find_by_id(self, cycle_id: str) -> LoopCycle | None:
        db_session = self.SessionLocal()
        try:
            db_model = (
                db_session.query(PostgresLoopCycleModel)
                .filter(PostgresLoopCycleModel.cycle_id == cycle_id)
                .first()
            )
            if not db_model:
                return None
            return LoopCycle(
                cycle_id=db_model.cycle_id,
                status=db_model.status,
                stage_executions=db_model.stage_executions_json,
                timestamp=db_model.timestamp,
            )
        finally:
            db_session.close()

    def list_all(self) -> list[LoopCycle]:
        db_session = self.SessionLocal()
        try:
            db_models = db_session.query(PostgresLoopCycleModel).all()
            return [
                LoopCycle(
                    cycle_id=m.cycle_id,
                    status=m.status,
                    stage_executions=m.stage_executions_json,
                    timestamp=m.timestamp,
                )
                for m in db_models
            ]
        finally:
            db_session.close()


class InMemoryAutonomousRepository(AutonomousRepository):
    """Adapter bộ nhớ RAM lưu trữ chu kỳ tiến hóa phục vụ kiểm thử di động."""

    # Đồng bộ chữ ký khởi tạo db_url để có thể hoán đổi cắm nóng (swap) cực kỳ mượt mà
    def __init__(self, db_url: str = "") -> None:
        self._store: dict[str, LoopCycle] = {}

    def save(self, cycle: LoopCycle) -> LoopCycle:
        self._store[cycle.cycle_id] = cycle
        return cycle

    def find_by_id(self, cycle_id: str) -> LoopCycle | None:
        return self._store.get(cycle_id)

    def list_all(self) -> list[LoopCycle]:
        return list(self._store.values())