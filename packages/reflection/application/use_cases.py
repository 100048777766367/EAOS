import uuid
from datetime import UTC, datetime

from packages.reflection.domain.models import (
    Recommendation,
    ReflectionReport,
    RootCause,
)
from packages.reflection.domain.ports import ReflectionRepository


class AnalyzeReflectionUseCase:
    """Application Service Ä‘iá»u phá»‘i cháº©n Ä‘oÃ¡n nguyÃªn nhÃ¢n gá»‘c sá»± cá»‘."""

    def __init__(self, repository: ReflectionRepository) -> None:
        self.repository = repository

    def execute(self, subject_id: str, trigger_event: str, passed_checks: bool) -> ReflectionReport:
        report_id = f"REF-{uuid.uuid4().hex[:6].upper()}"

        root_causes = []
        recommendations = []
        confidence = 1.0

        if not passed_checks:
            # Thuáº­t toÃ¡n tá»± suy ngáº«m nguyÃªn nhÃ¢n lá»—i ranh giá»›i phÃ¢n lá»›p
            root_causes.append(
                RootCause(
                    id="RC-01",
                    type="BoundaryViolation",
                    description=(
                        "PhÃ¡t hiá»‡n import sai lá»›p phÃ¢n tÃ¡ch. Táº§ng dÆ°á»›i "
                        "Ä‘ang phá»¥ thuá»™c trá»±c tiáº¿p vÃ o táº§ng trÃªn."
                    ),
                    probability=0.95,
                    evidence=[f"Module: {subject_id} contains illegal imports"],
                )
            )
            recommendations.append(
                Recommendation(
                    priority="HIGH",
                    action="Äiá»u hÆ°á»›ng láº¡i ranh giá»›i dependencies.",
                    reason=("Giá»¯ cho nhÃ¢n Kernel sáº¡ch sáº½, khÃ´ng bá»‹ phá»¥ thuá»™c vÃ o lá»›p ngoáº¡i biÃªn."),
                    risk="CÃ³ thá»ƒ tÄƒng nháº¹ thá»i gian refactor code.",
                )
            )
            confidence = 0.95
        else:
            # Náº¿u táº¥t cáº£ cÃ¡c ranh giá»›i Ä‘áº¡t chuáº©n tá»‘i Æ°u
            recommendations.append(
                Recommendation(
                    priority="LOW",
                    action="Duy trÃ¬ tráº¡ng thÃ¡i cáº¥u hÃ¬nh hiá»‡n táº¡i.",
                    reason="Táº¥t cáº£ cÃ¡c ranh giá»›i kiáº¿n trÃºc Ä‘áº¡t chuáº©n tá»‘i Æ°u.",
                    risk="KhÃ´ng cÃ³ rá»§i ro nÃ o Ä‘Æ°á»£c phÃ¡t hiá»‡n.",
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
