from abc import ABC, abstractmethod
from pathlib import Path  # Thêm import thiếu Path

from libs.validation.checker import ADRDocument
from pydantic import BaseModel


class RuleResult(BaseModel):
    rule_name: str
    passed: bool
    message: str
    details: list[str] = []


class ValidationRule(ABC):

    @abstractmethod
    def evaluate(
        self, dependency_graph: dict[str, set[str]], adrs: list[ADRDocument]
    ) -> RuleResult: ...


class HexagonalLayerIsolationRule(ValidationRule):
    """Đảm bảo các tầng nghiệp vụ tuân thủ ranh giới Hexagonal."""

    def evaluate(
        self, dependency_graph: dict[str, set[str]], adrs: list[ADRDocument]
    ) -> RuleResult:
        # Sửa lỗi PERF401 bằng cách sử dụng List Comprehension tối ưu
        violations = [
            (
                f"Layer Violation: '{pkg}' không được phụ thuộc ngược "
                f"vào lớp hạ tầng '{dep}'."
            )
            for pkg, deps in dependency_graph.items()
            for dep in deps
            if "domain" in pkg.lower() and "infrastructure" in dep.lower()
        ]

        if violations:
            return RuleResult(
                rule_name="Hexagonal Layer Isolation",
                passed=False,
                message=f"Phát hiện {len(violations)} vi phạm ranh giới phân lớp.",
                details=violations,
            )
        return RuleResult(
            rule_name="Hexagonal Layer Isolation",
            passed=True,
            message="Tất cả các ranh giới tuân thủ phân lớp Hexagonal.",
        )


class ADRStructureVerificationRule(ValidationRule):
    """Ép buộc mọi quyết định kỹ thuật phải tuân thủ Hiến pháp cấu trúc."""

    def evaluate(
        self, dependency_graph: dict[str, set[str]], adrs: list[ADRDocument]
    ) -> RuleResult:
        failures = []
        for adr in adrs:
            missing = []
            if not adr.has_status_header:
                missing.append("Status")
            if not adr.has_context_header:
                missing.append("Context")
            if not adr.has_decision_header:
                missing.append("Decision")
            if not adr.has_consequences_header:
                missing.append("Consequences")

            if missing:
                failures.append(
                    f"ADR '{adr.title}' ({Path(adr.file_path).name}) "
                    f"thiếu các mục bắt buộc: {', '.join(missing)}."
                )

        if failures:
            return RuleResult(
                rule_name="ADR Standardized Structure",
                passed=False,
                message="Phát hiện tệp tin ADR đặt sai quy chuẩn cấu trúc.",
                details=failures,
            )
        return RuleResult(
            rule_name="ADR Standardized Structure",
            passed=True,
            message="Tất cả các ADR tuân thủ chuẩn cấu trúc hiến pháp.",
        )