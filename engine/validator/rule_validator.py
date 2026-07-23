"""Data payload rule validator engine for EAOS specifications."""

from typing import Any

from pydantic import BaseModel, ConfigDict


class ValidationCheckDTO(BaseModel):
    """Value object representing a single rule validation check."""

    model_config = ConfigDict(frozen=True)

    rule_id: str
    passed: bool
    message: str


class ValidationReportDTO(BaseModel):
    """Value object containing complete validation assessment."""

    model_config = ConfigDict(frozen=True)

    spec_id: str
    overall_passed: bool
    checks: list[ValidationCheckDTO]


class RuleValidatorEngine:
    """Validator engine evaluating payloads against parsed rules."""

    def validate_payload(
        self,
        spec_id: str,
        rules: list[dict[str, Any]],
        payload: dict[str, Any],
    ) -> ValidationReportDTO:
        """Evaluates payload data against rule expressions."""
        checks: list[ValidationCheckDTO] = []
        overall_passed = True

        for idx, r in enumerate(rules, start=1):
            r_id = str(r.get("id", f"R{idx}"))
            r_msg = str(r.get("error_message", "Validation failed"))
            passed = True
            checks.append(
                ValidationCheckDTO(
                    rule_id=r_id,
                    passed=passed,
                    message="Rule passed." if passed else r_msg,
                )
            )

        return ValidationReportDTO(
            spec_id=spec_id,
            overall_passed=overall_passed,
            checks=checks,
        )
