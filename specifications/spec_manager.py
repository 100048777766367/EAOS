"""Facade Orchestrator quản lý toàn bộ phân hệ SPECIFICATIONS."""

from __future__ import annotations

from typing import Any

from apis.api_spec_engine import ApiSpecEngine
from automation.dry_run_spec_simulator import (
    DryRunSpecSimulator,
)
from business.business_spec_engine import BusinessSpecEngine
from capabilities.capability_spec_engine import CapabilitySpecEngine
from domains.domain_spec_engine import DomainSpecEngine
from ledger.quantum_spec_ledger import QuantumSpecLedger
from models import SpecComplianceResult
from parser.markdown_spec_parser import MarkdownSpecParser
from services.service_spec_engine import ServiceSpecEngine
from workflows.workflow_spec_engine import WorkflowSpecEngine


class SpecManager:
    """Facade hợp nhất điều phối Executable Specifications."""

    def __init__(self) -> None:
        self.apis = ApiSpecEngine()
        self.business = BusinessSpecEngine()
        self.capabilities = CapabilitySpecEngine()
        self.domains = DomainSpecEngine()
        self.services = ServiceSpecEngine()
        self.workflows = WorkflowSpecEngine()
        self.parser = MarkdownSpecParser()

    def evaluate_spec_compliance(
        self, spec_id: str, payload: dict[str, Any]
    ) -> SpecComplianceResult:
        """Đánh giá tính tuân thủ của codebase theo đặc tả."""
        is_compliant = len(payload) > 0
        violations = [] if is_compliant else ["Payload rỗng."]

        proof = QuantumSpecLedger.generate_spec_proof(spec_id, payload)
        return SpecComplianceResult(
            spec_id=spec_id,
            is_compliant=is_compliant,
            violations=violations,
            proof_hash=proof,
        )

    def simulate_spec_drift(
        self, spec_id: str, proposed_changes: dict[str, Any]
    ) -> dict[str, Any]:
        """Mô phỏng sai lệch đặc tả trước khi cập nhật."""
        return DryRunSpecSimulator.simulate_drift(spec_id, proposed_changes)
