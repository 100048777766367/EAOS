from dataclasses import dataclass, field
from enum import Enum, auto
from typing import Any


class PolicyEffect(Enum):
    ALLOW = auto()
    DENY = auto()


class Operator(Enum):
    EQUALS = auto()
    NOT_EQUALS = auto()
    GREATER_THAN = auto()
    LESS_THAN = auto()
    IN = auto()
    CONTAINS = auto()


@dataclass(frozen=True, slots=True)
class RuleCondition:
    field_path: str
    operator: Operator
    expected_value: Any

    def evaluate(self, context: dict[str, Any]) -> bool:
        actual = self._extract_field(context, self.field_path.split("."))
        if actual is None and self.expected_value is not None:
            return False

        match self.operator:
            case Operator.EQUALS:
                return bool(actual == self.expected_value)
            case Operator.NOT_EQUALS:
                return bool(actual != self.expected_value)
            case Operator.GREATER_THAN:
                return float(actual) > float(self.expected_value)
            case Operator.LESS_THAN:
                return float(actual) < float(self.expected_value)
            case Operator.IN:
                return bool(actual in self.expected_value)
            case Operator.CONTAINS:
                return bool(self.expected_value in actual)

    def _extract_field(self, data: Any, parts: list[str]) -> Any:
        if not parts or not isinstance(data, dict):
            return data
        key = parts[0]
        if key not in data:
            return None
        return self._extract_field(data[key], parts[1:])


@dataclass(frozen=True, slots=True)
class PolicyRule:
    rule_id: str
    name: str
    effect: PolicyEffect
    condition: RuleCondition
    failure_message: str


@dataclass(frozen=True, slots=True)
class EvaluationViolation:
    rule_id: str
    rule_name: str
    message: str


@dataclass(slots=True)
class PolicyDocumentAggregate:
    policy_id: str
    name: str
    description: str
    rules: list[PolicyRule] = field(default_factory=list)
    default_effect: PolicyEffect = PolicyEffect.DENY

    def add_rule(self, rule: PolicyRule) -> None:
        self.rules.append(rule)

    def evaluate(self, context: dict[str, Any]) -> tuple[bool, list[EvaluationViolation]]:
        violations: list[EvaluationViolation] = []

        for rule in self.rules:
            passed = rule.condition.evaluate(context)

            if (rule.effect == PolicyEffect.ALLOW and not passed) or (rule.effect == PolicyEffect.DENY and passed):
                violations.append(
                    EvaluationViolation(
                        rule_id=rule.rule_id,
                        rule_name=rule.name,
                        message=rule.failure_message,
                    )
                )

        is_allowed = len(violations) == 0
        return is_allowed, violations
