from datetime import UTC, datetime
from pathlib import Path

from pydantic import BaseModel, ConfigDict, Field


class LoopTrigger(BaseModel):
    """Tín hiệu kích hoạt vòng phản hồi (Feedback Loop Trigger)."""

    loop_type: str  # "EXECUTION", "ARCHITECTURE", "STRATEGY"
    cadence: str  # "FAST" (Minutes/Hours), "MEDIUM" (Weeks/Months), "SLOW" (Years)
    trigger_context: str
    timestamp: datetime = Field(default_factory=lambda: datetime.now(UTC))

    model_config = ConfigDict(frozen=True)


class LoopExecution(BaseModel):
    """Bản ghi kiểm toán và ép buộc tuân thủ của Vòng phản hồi."""

    loop_type: str
    cadence: str
    status: str  # "COMPLETED", "FAILED"
    evidence_logs: list[str] = Field(default_factory=list)
    timestamp: datetime = Field(default_factory=lambda: datetime.now(UTC))

    model_config = ConfigDict(frozen=True)


class GovernanceLoopEngine:
    """Hệ điều hành kiểm soát 3 Vòng phản hồi lồng nhau (Three Nested Loops)."""

    def __init__(self, root_dir: Path) -> None:
        self.root_dir = root_dir
        self.docs_dir = root_dir / "docs"

    def evaluate_loop(self, trigger: LoopTrigger) -> LoopExecution:
        logs = []
        status = "COMPLETED"

        if trigger.loop_type == "EXECUTION":
            # 1. Execution Loop (Fast - Nhịp: Phút/Giờ)
            # Thẩm định tệp TASK.md hằng ngày
            task_file = self.docs_dir / "TASK.md"
            if not task_file.exists():
                status = "FAILED"
                logs.append("Lỗi: Không tìm thấy tệp 'docs/TASK.md' gác cổng.")
            else:
                content = task_file.read_text(encoding="utf-8")
                if "[ ]" not in content and "[x]" not in content:
                    status = "FAILED"
                    logs.append("Lỗi: Không phát hiện danh mục nhiệm vụ.")
                else:
                    logs.append("Execution Loop: TASK.md parsed successfully.")

        elif trigger.loop_type == "ARCHITECTURE":
            # 2. Architecture Evolution Loop (Medium - Nhịp: Tuần/Tháng)
            # Thẩm định hiến pháp và chỉ mục quyết định kiến trúc (ADRs)
            const_file = self.docs_dir / "ARCHITECTURE_CONSTITUTION.md"
            meta_file = self.docs_dir / "architecture" / "EAOS_META_ARCHITECTURE.md"
            adr_dir = self.docs_dir / "decisions"

            if not const_file.exists():
                status = "FAILED"
                logs.append("Lỗi: Khuyết thiếu tệp hiến pháp tối cao.")
            if not meta_file.exists():
                status = "FAILED"
                logs.append("Lỗi: Khuyết thiếu tệp kiến trúc hệ thống.")
            if not adr_dir.exists() or not list(adr_dir.glob("*.md")):
                status = "FAILED"
                logs.append("Lỗi: Chưa đăng ký tài liệu quyết định kỹ thuật ADR.")

            if status == "COMPLETED":
                logs.append("Architecture Loop: Constitution & ADRs verified.")

        elif trigger.loop_type == "STRATEGY":
            # 3. Strategic Evolution Loop (Slow - Nhịp: Năm)
            # Thẩm định ROADMAP.md và PROJECT_CONTEXT.md
            roadmap_file = self.docs_dir / "ROADMAP.md"
            context_file = self.docs_dir / "PROJECT_CONTEXT.md"

            if not roadmap_file.exists():
                status = "FAILED"
                logs.append("Lỗi: Khuyết thiếu tệp ROADMAP.md.")
            if not context_file.exists():
                status = "FAILED"
                logs.append("Lỗi: Khuyết thiếu tệp PROJECT_CONTEXT.md.")

            if status == "COMPLETED":
                logs.append("Strategy Loop: Vision & Roadmap verified.")

        else:
            status = "FAILED"
            logs.append(f"Lỗi: Phân loại vòng lặp '{trigger.loop_type}' không tồn tại.")

        return LoopExecution(
            loop_type=trigger.loop_type,
            cadence=trigger.cadence,
            status=status,
            evidence_logs=logs,
            timestamp=datetime.now(UTC),
        )
