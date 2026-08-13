"""Application use cases for EAOS Judicial Court & Legal Trial."""

import sys
import uuid
from pathlib import Path

ROOT_PATH = Path(__file__).resolve().parent.parent.parent.parent
if str(ROOT_PATH) not in sys.path:
    sys.path.insert(0, str(ROOT_PATH))

from packages.legal_governance.domain.models import (  # noqa: E402
    LegalVerdictDTO,
)


class ConductArchitecturalTrialUseCase:
    """Use case executing a legal trial against code violations."""

    def execute(
        self,
        target_artifact: str,
        has_violation: bool,
        defense_argument: str,
    ) -> LegalVerdictDTO:
        """Executes trial, evaluates defense, and issues binding verdict."""
        trial_id = f"TRIAL-{uuid.uuid4().hex[:8].upper()}"
        if has_violation and "REMEDIATED" not in defense_argument:
            verdict_str = "GUILTY_VIOLATION"
            action = "QUARANTINE_WASM_SANDBOX"
        else:
            verdict_str = "ACQUITTED_COMPLIANT"
            action = "APPROVED_MERGE"

        return LegalVerdictDTO(
            trial_id=trial_id,
            target_artifact=target_artifact,
            verdict=verdict_str,
            sanction_action=action,
            evidence_hash=f"sha256_{uuid.uuid4().hex[:16]}",
        )


if __name__ == "__main__":
    uc = ConductArchitecturalTrialUseCase()
    verdict = uc.execute("packages/domain/models.py", True, "REMEDIATED AST")
    print(f"✔ Legal Trial Verdict: {verdict.verdict} -> {verdict.sanction_action}")
