from abc import ABC, abstractmethod

from pydantic import BaseModel

from packages.evolution.domain.models import EvolutionObject


class RuleResult(BaseModel):
    """Kết quả kiểm thử của một luật cụ thể."""

    rule_name: str
    passed: bool
    message: str


class Rule(ABC):
    """Lớp trừu tượng cho mọi quy tắc kiến trúc cấp cao."""

    @abstractmethod
    def evaluate(self, obj: EvolutionObject) -> RuleResult: ...


class VersionHeaderRule(Rule):
    """Quy tắc bắt buộc mọi cấu hình tiến hóa phải có số phiên bản."""

    def evaluate(self, obj: EvolutionObject) -> RuleResult:
        version = obj.payload.get("__version")
        if version is None:
            return RuleResult(
                rule_name="VersionHeaderRule",
                passed=False,
                message="Khóa '__version' bị thiếu trong payload cấu hình.",
            )
        return RuleResult(
            rule_name="VersionHeaderRule",
            passed=True,
            message=f"Khóa '__version' hợp chuẩn, giá trị: {version}.",
        )


class CriticalityEnvironmentRule(Rule):
    """Môi trường production bắt buộc độ nghiêm trọng phải là high."""

    def evaluate(self, obj: EvolutionObject) -> RuleResult:
        env = obj.metadata.environment
        crit = obj.metadata.criticality
        if env == "production" and crit != "high":
            return RuleResult(
                rule_name="CriticalityEnvironmentRule",
                passed=False,
                message="Môi trường production yêu cầu criticality='high'.",
            )
        return RuleResult(
            rule_name="CriticalityEnvironmentRule",
            passed=True,
            message="Mức độ nghiêm trọng phù hợp với môi trường sản xuất.",
        )


class PolicyEngine:
    """Động cơ gom các luật (Rules) thành các Chính sách lớn (Policies)."""

    def __init__(self, name: str, rules: list[Rule]) -> None:
        self.name = name
        self.rules = rules

    def evaluate_policy(self, obj: EvolutionObject) -> tuple[bool, list[RuleResult]]:
        passed = True
        results = []
        for rule in self.rules:
            res = rule.evaluate(obj)
            results.append(res)
            if not res.passed:
                passed = False
        return passed, results


class FitnessEngine:
    """Động cơ phân tích điểm thể lực kiến trúc từ các bằng chứng (Evidence)."""

    @staticmethod
    def calculate_fitness(obj: EvolutionObject) -> float:
        if not obj.evidences:
            return 0.0
        passed_evidences = [ev for ev in obj.evidences if ev.passed]
        return len(passed_evidences) / len(obj.evidences)
