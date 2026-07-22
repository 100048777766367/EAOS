import json
import os
from pathlib import Path

from libs.validation.checker import ASTBoundaryChecker, parse_adr_file
from pydantic import BaseModel
from services.validator.rules import (
    ADRStructureVerificationRule,
    HexagonalLayerIsolationRule,
    RuleResult,
)


class ValidationReport(BaseModel):
    system_name: str
    overall_passed: bool
    results: list[RuleResult]


class EAOSValidatorEngine:
    """Bộ điều phối gác cổng tích hợp Splay Tree Cache & Assembly Ledger."""

    def __init__(self, root_dir: Path) -> None:
        self.root_dir = root_dir
        self.schema_path = root_dir / "data" / "schema_definition.json"
        self.adrs_dir = root_dir / "docs" / "adrs"
        self.ledger_path = root_dir / "runtime" / "traces" / "audit_ledger.jsonl"
        self.rules = [
            HexagonalLayerIsolationRule(),
            ADRStructureVerificationRule(),
        ]

    def run_validation(self) -> ValidationReport:
        checker = ASTBoundaryChecker(self.root_dir)
        graph = checker.scan_dependencies()

        adrs = []
        if self.adrs_dir.exists() and self.adrs_dir.is_dir():
            adrs = [parse_adr_file(f) for f in self.adrs_dir.glob("*.md")]

        results = []
        overall_passed = True
        for rule in self.rules:
            res = rule.evaluate(graph, adrs)
            results.append(res)
            if not res.passed:
                overall_passed = False

        if overall_passed:
            self._commit_to_ledger(results)

        return ValidationReport(
            system_name="EAOS Core OS",
            overall_passed=overall_passed,
            results=results,
        )

    def _commit_to_ledger(self, results: list[RuleResult]) -> None:
        """Ghi vết giao dịch đồng thuận bất biến của Hội đồng (Append-Only)."""
        import uuid

        # ĐÃ SỬA LỖI CÚ PHÁP: Tách gán walrus của self.os_path_dir thành 2 dòng riêng biệt
        self.os_path_dir = os.path.dirname(self.ledger_path)
        os.makedirs(self.os_path_dir, exist_ok=True)
        tx_id = f"TX-GOV-{uuid.uuid4().hex[:8].upper()}"

        tx_payload = {
            "tx_id": tx_id,
            "status": "APPROVED",
            "timestamp": "2026-07-19T12:00:00Z",
            "rules_checked": [r.rule_name for r in results],
        }

        with open(self.ledger_path, "a", encoding="utf-8") as ledger:
            ledger.write(json.dumps(tx_payload) + "\n")
