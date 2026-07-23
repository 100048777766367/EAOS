"""Constitutional Amendment Engine governed by BFT Synod quorum voting."""

import json
import uuid
from pathlib import Path
from typing import Any

from pydantic import BaseModel, ConfigDict


class AmendmentProposal(BaseModel):
    """Value object representing a constitutional amendment proposal."""

    model_config = ConfigDict(frozen=True)

    amendment_id: str
    target_rule: str
    proposed_text: str
    reasoning: str


class AmendmentResult(BaseModel):
    """Value object representing constitutional amendment ratification outcome."""

    model_config = ConfigDict(frozen=True)

    amendment_id: str
    ratified: bool
    effective_version: str
    audit_tx_id: str


class ConstitutionalAmendmentEngine:
    """Engine governing constitutional amendments via BFT Synod voting."""

    def __init__(
        self,
        ledger_path: str = "runtime/traces/audit_ledger.jsonl",
    ) -> None:
        self.ledger_path = Path(ledger_path)

    def submit_amendment(
        self,
        proposal: AmendmentProposal,
        synod_votes: list[dict[str, Any]],
    ) -> AmendmentResult:
        """Evaluates BFT quorum and ratifies amendment if approved."""
        total_nodes = len(synod_votes) if synod_votes else 4
        fault_tolerance = (total_nodes - 1) // 3
        required_approvals = (2 * fault_tolerance) + 1

        approvals = sum(1 for v in synod_votes if v.get("decision") == "APPROVE")
        ratified = approvals >= required_approvals

        tx_id = f"TX-AMEND-{uuid.uuid4().hex[:8].upper()}"
        if ratified:
            self._record_ledger_entry(tx_id, proposal, approvals)

        version_str = "ARCHITECTURE_CONSTITUTION_v2.1" if ratified else "v2.0"

        return AmendmentResult(
            amendment_id=proposal.amendment_id,
            ratified=ratified,
            effective_version=version_str,
            audit_tx_id=tx_id,
        )

    def _record_ledger_entry(
        self,
        tx_id: str,
        proposal: AmendmentProposal,
        approvals: int,
    ) -> None:
        """Appends ratified amendment transaction to audit ledger."""
        self.ledger_path.parent.mkdir(parents=True, exist_ok=True)
        entry = {
            "tx_id": tx_id,
            "action": "CONSTITUTIONAL_AMENDMENT_RATIFIED",
            "timestamp": "2026-07-23T05:10:00Z",
            "amendment_id": proposal.amendment_id,
            "target_rule": proposal.target_rule,
            "approvals": approvals,
        }
        with self.ledger_path.open("a", encoding="utf-8") as f:
            f.write(json.dumps(entry) + "\n")
