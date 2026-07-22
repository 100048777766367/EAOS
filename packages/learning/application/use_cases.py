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
    """Application Service Ä‘iá»u phá»‘i viá»‡c chuyá»ƒn dá»‹ch cháº©n Ä‘oÃ¡n thÃ nh Kinh nghiá»‡m."""

    def __init__(
        self,
        exp_repo: ExperienceRepository,
        reflection_repo: ReflectionRepository,
    ) -> None:
        self.exp_repo = exp_repo
        self.reflection_repo = reflection_repo

    def execute(self, reflection_id: str) -> Experience:
        # 1. TÃ¬m kiáº¿m bÃ¡o cÃ¡o cháº©n Ä‘oÃ¡n sá»± cá»‘ gá»‘c
        report = self.reflection_repo.find_by_id(reflection_id)
        if not report:
            raise ValueError(f"BÃ¡o cÃ¡o cháº©n Ä‘oÃ¡n {reflection_id} khÃ´ng tá»“n táº¡i.")

        exp_id = f"EXP-{uuid.uuid4().hex[:6].upper()}"

        # 2. Ãp dá»¥ng List Comprehensions giáº£i quyáº¿t PERF401 & F841
        lessons = [
            Lesson(
                id="L-01",
                takeaway=("KhÃ´ng bao giá» Ä‘á»ƒ táº§ng Domain phá»¥ thuá»™c vÃ o Infrastructure."),
                action_item="Sá»­ dá»¥ng Ports & Adapters Ä‘á»ƒ Ä‘áº£o ngÆ°á»£c phá»¥ thuá»™c.",
            )
            for rc in report.root_causes
            if rc.type == "BoundaryViolation"
        ]

        anti_patterns = [
            AntiPattern(
                id="AP-01",
                name="Database Leak in Domain",
                avoid_reason="LÃ m bÃ¡m cháº·t mÃ£ nguá»“n vÃ o thÆ° viá»‡n cÆ¡ sá»Ÿ dá»¯ liá»‡u.",
            )
            for rc in report.root_causes
            if rc.type == "BoundaryViolation"
        ]

        patterns = [
            Pattern(
                id="PT-01",
                name="Hexagonal Boundary Protection",
                description="Bá»c ngoÃ i báº±ng Ports Ä‘á»ƒ cÃ´ láº­p nhÃ¢n nghiá»‡p vá»¥.",
            )
            for rc in report.root_causes
            if rc.type == "BoundaryViolation"
        ]

        heuristics = [
            Heuristic(
                id="H-01",
                rule_of_thumb=(
                    "Náº¿u lá»›p Domain cÃ³ import sqlalchemy, cháº·n ngay láº­p tá»©c."
                ),
                applicability="CI/CD Linter Checks",
            )
            for rc in report.root_causes
            if rc.type == "BoundaryViolation"
        ]

        # 3. ÄÃ³ng gÃ³i thÃ nh Experience hoÃ n chá»‰nh
        exp = Experience(
            id=exp_id,
            reflection_id=reflection_id,
            title=f"Kinh nghiá»‡m tá»« sá»± cá»‘: {report.subject}",
            lessons=lessons,
            patterns=patterns,
            anti_patterns=anti_patterns,
            heuristics=heuristics,
            created_at=datetime.now(UTC),
        )

        return self.exp_repo.save(exp)

