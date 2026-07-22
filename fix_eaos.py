import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parent

print("==========================================================")
print(" EAOS ULTIMATE MYPY & INTEGRATION TEST SELF-HEALING       ")
print("==========================================================")

# 1. PLATFORM SERVICES RESILIENCE ENGINE (ĐỊNH NGHĨA TẬP TRUNG IDEMPOTENCYMANAGER)
res_engine_path = ROOT / "platform_services" / "resilience" / "engine.py"
res_engine_content = '''import time
from typing import Any, Callable


class IdempotencyManager:
    """Manages request idempotency keys to prevent duplicate execution."""

    def __init__(self) -> None:
        self._cache: dict[str, Any] = {}

    def check_and_set(
        self, key: str, payload: Any
    ) -> tuple[bool, Any]:
        if key in self._cache:
            return True, self._cache[key]
        self._cache[key] = payload
        return False, payload


class IdempotencyService:
    """Service wrapper for idempotent function processing."""

    def __init__(self) -> None:
        self._cache: dict[str, Any] = {}

    def process(
        self, key: str, func: Callable[..., Any], *args: Any, **kwargs: Any
    ) -> Any:
        if key in self._cache:
            return self._cache[key]
        result = func(*args, **kwargs)
        self._cache[key] = result
        return result


class ResilienceEngine:
    """Provides automated exponential backoff and retry execution."""

    def __init__(
        self, max_retries: int = 3, backoff_factor: float = 0.1
    ) -> None:
        self.max_retries = max_retries
        self.backoff_factor = backoff_factor

    def execute_with_retry(
        self, func: Callable[..., Any], *args: Any, **kwargs: Any
    ) -> Any:
        last_error: Exception | None = None
        for attempt in range(self.max_retries):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                last_error = e
                time.sleep(self.backoff_factor * (2**attempt))
        raise RuntimeError(
            f"Retry limit ({self.max_retries}) exceeded. Error: {last_error}"
        ) from last_error
'''
res_engine_path.write_text(res_engine_content, encoding="utf-8")
print("✔ 1. Sửa platform_services/resilience/engine.py (Đã thêm IdempotencyManager).")

# 2. EVOLUTION USE CASES (BỔ SUNG IMPORT ANY)
evo_uc_path = ROOT / "packages" / "evolution" / "application" / "use_cases.py"
text_evo = evo_uc_path.read_text(encoding="utf-8")
if "from typing import Any" not in text_evo:
    text_evo = "from typing import Any\n" + text_evo
text_evo = text_evo.replace("payload: dict,", "payload: dict[str, Any],")
text_evo = text_evo.replace("rules: dict,", "rules: dict[str, Any],")
evo_uc_path.write_text(text_evo, encoding="utf-8")
print("✔ 2. Sửa packages/evolution/application/use_cases.py (Đã thêm 'from typing import Any').")

# 3. POLICY ENGINE DOMAIN MODELS
pol_path = ROOT / "packages" / "policy_engine" / "domain" / "models.py"
pol_content = '''from dataclasses import dataclass, field
from datetime import datetime, timezone
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

    def evaluate(
        self, context: dict[str, Any]
    ) -> tuple[bool, list[EvaluationViolation]]:
        violations: list[EvaluationViolation] = []

        for rule in self.rules:
            passed = rule.condition.evaluate(context)

            if rule.effect == PolicyEffect.ALLOW and not passed:
                violations.append(
                    EvaluationViolation(
                        rule_id=rule.rule_id,
                        rule_name=rule.name,
                        message=rule.failure_message,
                    )
                )
            elif rule.effect == PolicyEffect.DENY and passed:
                violations.append(
                    EvaluationViolation(
                        rule_id=rule.rule_id,
                        rule_name=rule.name,
                        message=rule.failure_message,
                    )
                )

        is_allowed = len(violations) == 0
        return is_allowed, violations
'''
pol_path.write_text(pol_content, encoding="utf-8")
print("✔ 3. Sửa packages/policy_engine/domain/models.py.")

# 4. DỌN UTF-8 BOMS
for p in ROOT.rglob("*.py"):
    if p.is_file() and ".venv" not in p.parts:
        try:
            c = p.read_text(encoding="utf-8-sig")
            p.write_text(c, encoding="utf-8")
        except Exception:
            pass
print("✔ 4. Đã dọn sạch UTF-8 BOM.")

print("\n>>> THỰC THI KIỂM TOÁN TỰ ĐỘNG...")
subprocess.run(["uv", "sync"], check=False)
subprocess.run(["uv", "run", "task", "lint"], check=False)
subprocess.run(["uv", "run", "task", "test"], check=False)
subprocess.run(["uv", "run", "task", "validate"], check=False)