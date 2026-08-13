"""Contradiction Filter Engine for Claim Invalidation over Turns."""

from __future__ import annotations

from typing import Final

from provenance.domain.models import ClaimValidityDTO


class ContradictionFilter:
    """Invalidates old claims when a newer turn overrides them."""

    def __init__(self) -> None:
        self._claims: Final[list[ClaimValidityDTO]] = []

    def record_claim(
        self,
        subject: str,
        predicate: str,
        object_val: str,
        source_turn_id: int,
    ) -> ClaimValidityDTO:
        """Records a claim and invalidates conflicting old claims."""
        for idx, old in enumerate(self._claims):
            if (
                old.subject.lower() == subject.lower()
                and old.predicate.lower() == predicate.lower()
                and old.valid_to_turn is None
            ):
                self._claims[idx] = old.model_copy(update={"valid_to_turn": source_turn_id - 1})

        claim_id = f"claim-{len(self._claims) + 1}"
        new_claim = ClaimValidityDTO(
            claim_id=claim_id,
            subject=subject,
            predicate=predicate,
            object_val=object_val,
            valid_from_turn=source_turn_id,
            valid_to_turn=None,
            source_turn_id=source_turn_id,
        )
        self._claims.append(new_claim)
        return new_claim

    def get_active_claims(self, current_turn_id: int | None = None) -> list[ClaimValidityDTO]:
        """Returns active claims for a given turn."""
        active: list[ClaimValidityDTO] = []
        for claim in self._claims:
            if current_turn_id is not None:
                if claim.valid_from_turn <= current_turn_id and (
                    claim.valid_to_turn is None or claim.valid_to_turn >= current_turn_id
                ):
                    active.append(claim)
            elif claim.valid_to_turn is None:
                active.append(claim)
        return active
