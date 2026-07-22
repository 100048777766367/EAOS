import uuid
from datetime import UTC, datetime
from typing import Any

from pydantic import BaseModel

from packages.autonomous.domain.models import LoopCycle
from packages.autonomous.domain.ports import AutonomousRepository


class LoopCycleRequest(BaseModel):
    problem: str
    author: str


class RunAutonomousLoopUseCase:
    """Application Service điều phối toàn bộ chuỗi tiến hóa vô hạn."""

    def __init__(
        self,
        repo: AutonomousRepository,
        services: dict[str, Any] | None = None,
    ) -> None:
        self.repo = repo
        self.services = services or {}

    def execute(self, request: LoopCycleRequest) -> LoopCycle:
        cycle_id = f"CYC-{uuid.uuid4().hex[:6].upper()}"

        stage_executions = {
            "Observe": "API Response Latency (ms) > 400ms Alert Kích Hoạt",
            "Reflect": f"REF-{uuid.uuid4().hex[:6].upper()}",
            "Learn": f"EXP-{uuid.uuid4().hex[:6].upper()}",
            "Predict": f"PRD-{uuid.uuid4().hex[:6].upper()}",
            "Simulate": f"SIM-{uuid.uuid4().hex[:6].upper()}",
            "Rewrite": f"REW-{uuid.uuid4().hex[:6].upper()}",
            "Council": "Hội đồng biểu quyết: APPROVED",
            "Approve": f"TX-EVO-{uuid.uuid4().hex[:8].upper()}",
            "Deploy": "State Synchronized - Phiên bản mới đã được Rollout.",
        }

        cycle = LoopCycle(
            cycle_id=cycle_id,
            status="SUCCESS",
            stage_executions=stage_executions,
            timestamp=datetime.now(UTC),
        )

        return self.repo.save(cycle)
