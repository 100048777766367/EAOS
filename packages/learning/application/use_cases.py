import uuid
from datetime import UTC, datetime

from packages.learning.domain.models import (
    AntiPattern,
    Experience,
    Heuristic,
    Lesson,
    Pattern,
)
from packages.learning.domain.ports import ExperienceRepository
from packages.reflection.domain.ports import ReflectionRepository


class IngestLearningUseCase:
    """Application Service điều phối việc chuyển dịch chẩn đoán thành Kinh nghiệm."""

    def __init__(
        self,
        exp_repo: ExperienceRepository,
        reflection_repo: ReflectionRepository,
    ) -> None:
        self.exp_repo = exp_repo
        self.reflection_repo = reflection_repo

    def execute(self, reflection_id: str) -> Experience:
        # 1. Tìm kiếm báo cáo chẩn đoán sự cố gốc
        report = self.reflection_repo.find_by_id(reflection_id)
        if not report:
            raise ValueError(f"Báo cáo chẩn đoán {reflection_id} không tồn tại.")

        exp_id = f"EXP-{uuid.uuid4().hex[:6].upper()}"

        # 2. Áp dụng List Comprehensions giải quyết PERF401 & F841
        lessons = [
            Lesson(
                id="L-01",
                takeaway=(
                    "Không bao giờ để tầng Domain phụ thuộc vào "
                    "Infrastructure."
                ),
                action_item="Sử dụng Ports & Adapters để đảo ngược phụ thuộc.",
            )
            for rc in report.root_causes
            if rc.type == "BoundaryViolation"
        ]

        anti_patterns = [
            AntiPattern(
                id="AP-01",
                name="Database Leak in Domain",
                avoid_reason="Làm bám chặt mã nguồn vào thư viện cơ sở dữ liệu.",
            )
            for rc in report.root_causes
            if rc.type == "BoundaryViolation"
        ]

        patterns = [
            Pattern(
                id="PT-01",
                name="Hexagonal Boundary Protection",
                description="Bọc ngoài bằng Ports để cô lập nhân nghiệp vụ.",
            )
            for rc in report.root_causes
            if rc.type == "BoundaryViolation"
        ]

        heuristics = [
            Heuristic(
                id="H-01",
                rule_of_thumb=(
                    "Nếu lớp Domain có import sqlalchemy, "
                    "chặn ngay lập tức."
                ),
                applicability="CI/CD Linter Checks",
            )
            for rc in report.root_causes
            if rc.type == "BoundaryViolation"
        ]

        # 3. Đóng gói thành Experience hoàn chỉnh
        exp = Experience(
            id=exp_id,
            reflection_id=reflection_id,
            title=f"Kinh nghiệm từ sự cố: {report.subject}",
            lessons=lessons,
            patterns=patterns,
            anti_patterns=anti_patterns,
            heuristics=heuristics,
            created_at=datetime.now(UTC),
        )

        return self.exp_repo.save(exp)