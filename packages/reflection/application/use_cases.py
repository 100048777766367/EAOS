import uuid
from datetime import UTC, datetime

from packages.reflection.domain.models import (
    Recommendation,
    ReflectionReport,
    RootCause,
)
from packages.reflection.domain.ports import ReflectionRepository


class AnalyzeReflectionUseCase:
    """Application Service điều phối chẩn đoán nguyên nhân gốc sự cố."""

    def __init__(self, repository: ReflectionRepository) -> None:
        self.repository = repository

    def execute(
        self, subject_id: str, trigger_event: str, passed_checks: bool
    ) -> ReflectionReport:
        report_id = f"REF-{uuid.uuid4().hex[:6].upper()}"

        root_causes = []
        recommendations = []
        confidence = 1.0

        if not passed_checks:
            # Thuật toán tự suy ngẫm nguyên nhân lỗi ranh giới phân lớp
            root_causes.append(
                RootCause(
                    id="RC-01",
                    type="BoundaryViolation",
                    description=(
                        "Phát hiện import sai lớp phân tách. Tầng dưới "
                        "đang phụ thuộc trực tiếp vào tầng trên."
                    ),
                    probability=0.95,
                    evidence=[f"Module: {subject_id} contains illegal imports"],
                )
            )
            recommendations.append(
                Recommendation(
                    priority="HIGH",
                    action="Điều hướng lại ranh giới dependencies.",
                    reason=(
                        "Giữ cho nhân Kernel sạch sẽ, không bị phụ thuộc "
                        "vào lớp ngoại biên."
                    ),
                    risk="Có thể tăng nhẹ thời gian refactor code.",
                )
            )
            confidence = 0.95
        else:
            # Nếu tất cả các ranh giới đạt chuẩn tối ưu
            recommendations.append(
                Recommendation(
                    priority="LOW",
                    action="Duy trì trạng thái cấu hình hiện tại.",
                    reason="Tất cả các ranh giới kiến trúc đạt chuẩn tối ưu.",
                    risk="Không có rủi ro nào được phát hiện.",
                )
            )
            confidence = 1.0

        report = ReflectionReport(
            id=report_id,
            subject=subject_id,
            trigger=trigger_event,
            root_causes=root_causes,
            confidence=confidence,
            recommendations=recommendations,
            created_at=datetime.now(UTC),
        )

        return self.repository.save(report)