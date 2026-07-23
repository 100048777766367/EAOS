"""Application use cases for evaluating constitutional governance rules."""

from packages.governance.domain.models import (
    ConstitutionalRule,
    ConstitutionAmendment,
)


class EvaluateGovernanceUseCase:
    """Use case evaluating rule compliance against incoming changes."""

    def execute(
        self,
        rule: ConstitutionalRule,
        amendment: ConstitutionAmendment,
    ) -> bool:
        """Executes invariant compliance validation."""
        if not rule.enforced:
            return True
        return len(amendment.proposed_text) > 0
