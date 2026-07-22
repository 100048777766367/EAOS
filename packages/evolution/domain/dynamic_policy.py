from pathlib import Path
from typing import Any

import yaml  # type: ignore[import-untyped]
from pydantic import BaseModel, ConfigDict


class DynamicRuleResult(BaseModel):
    """Kết quả đánh giá của từng quy tắc chính sách động."""

    rule_id: str
    passed: bool
    message: str

    model_config = ConfigDict(frozen=True)


class DynamicPolicyEvaluator:
    """Động cơ đánh giá chính sách khai báo nạp nóng 0-downtime."""

    def __init__(self, policy_path: str | Path) -> None:
        self.policy_path: Path = Path(policy_path)
        self.policy_data: dict[str, Any] = {}
        self.reload_policy()

    def reload_policy(self) -> None:
        """Đọc lại tệp hoặc quét thư mục chính sách từ đĩa cứng mà không cần restart Gateway."""
        if self.policy_path.is_file():
            with open(self.policy_path, encoding="utf-8") as f:
                self.policy_data = yaml.safe_load(f) or {}
        elif self.policy_path.is_dir():
            merged_rules: list[dict[str, Any]] = []
            merged_data: dict[str, Any] = {"rules": merged_rules}
            policy_files = list(self.policy_path.rglob("*.yaml")) + list(self.policy_path.rglob("*.yml"))
            for file_path in policy_files:
                with open(file_path, encoding="utf-8") as f:
                    data = yaml.safe_load(f) or {}
                    if "name" in data and "name" not in merged_data:
                        merged_data["name"] = data["name"]
                    if "rules" in data and isinstance(data["rules"], list):
                        merged_rules.extend(data["rules"])
            self.policy_data = merged_data
        else:
            self.policy_data = {}

    reload_policies = reload_policy

    def evaluate_payload(self, payload: dict[str, Any]) -> tuple[bool, list[DynamicRuleResult]]:
        """Thực thi kiểm toán các quy tắc khai báo động trên payload."""
        results: list[DynamicRuleResult] = []
        overall_passed = True

        rules = self.policy_data.get("rules", [])
        for rule in rules:
            rule_id = rule.get("id", "UNKNOWN-RULE")
            field = rule.get("field")
            operator = rule.get("operator")
            expected_val = rule.get("value")
            err_msg = rule.get("error_message", "Chính sách vi phạm.")

            passed = True
            if operator == "EXISTS":
                passed = field in payload
            elif operator == "NOT_EXISTS":
                passed = field not in payload
            elif operator == "GREATER_THAN_OR_EQUAL":
                val = payload.get(field, 0)
                passed = isinstance(val, (int, float)) and val >= expected_val

            if not passed:
                overall_passed = False

            results.append(
                DynamicRuleResult(
                    rule_id=rule_id,
                    passed=passed,
                    message="Đạt chuẩn" if passed else err_msg,
                )
            )

        return overall_passed, results
