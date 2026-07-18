import uuid
from datetime import UTC, datetime

from packages.reflection.domain.ports import ReflectionRepository
from packages.learning.domain.models import (
    AntiPattern,
    Experience,
    Heuristic,
    Lesson,
    Pattern,
)
from packages.learning.domain.ports import ExperienceRepository


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
        lessons = []
        patterns = []
        anti_patterns = []
        heuristics = []

        # 2. Phân tích nguyên nhân để đúc rút tri thức học tập
        for rc in report.root_causes:
            if rc.type == "BoundaryViolation":
                lessons.append(
                    Lesson(
                        id="L-01",
                        takeaway=(
                            "Không bao giờ để tầng Domain phụ thuộc vào "