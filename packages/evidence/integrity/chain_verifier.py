"""Cryptographic Evidence Canonical Hash Chain Verifier v2 (Item 4 & 17 Fix)."""

from __future__ import annotations

from packages.evidence.adapters.hashing.sha256_evidence_hasher import (
    SHA256EvidenceHasherAdapter,
)
from packages.evidence.domain.evidence import Evidence
from packages.evidence.integrity.audit_event import (
    IntegrityFailureAuditEventDTO,
)


class ChainVerifier:
    """Verifies Genesis link (first link previous_hash None), bound hashes and sequence."""

    def __init__(self) -> None:
        self.hasher = SHA256EvidenceHasherAdapter()
        self.audit_events: list[IntegrityFailureAuditEventDTO] = []

    def verify_chain(self, evidences: list[Evidence]) -> tuple[bool, list[IntegrityFailureAuditEventDTO]]:
        """Returns (is_valid, list_of_audit_events)."""
        if not evidences:
            return True, []

        events: list[IntegrityFailureAuditEventDTO] = []

        # Item 4 Fix: First evidence in chain MUST have previous_hash == None (Genesis)
        first = evidences[0]
        if first.integrity.previous_hash is not None:
            evt = IntegrityFailureAuditEventDTO(
                event_id=f"audit-gen-{first.evidence_id.value}",
                evidence_id=first.evidence_id.value,
                failure_type="GENESIS_BREACH",
                details=(
                    f"First evidence '{first.evidence_id.value}' in session "
                    f"must have previous_hash=None, but found "
                    f"'{first.integrity.previous_hash}'."
                ),
            )
            events.append(evt)
            self.audit_events.append(evt)
            return False, events

        for i, ev in enumerate(evidences):
            canon_calc, chain_calc = self.hasher.calculate_canonical_hash(
                evidence_id=ev.evidence_id.value,
                evidence_type=ev.evidence_type.value,
                user_id=ev.user_id,
                session_id=ev.session_id,
                turn_id=ev.turn_id,
                raw_content=ev.content.raw_content,
                metadata_str=str(ev.metadata.entries),
                previous_hash=ev.integrity.previous_hash,
            )

            if ev.integrity.canonical_hash != canon_calc or ev.integrity.chain_hash != chain_calc:
                evt = IntegrityFailureAuditEventDTO(
                    event_id=f"audit-tamper-{ev.evidence_id.value}",
                    evidence_id=ev.evidence_id.value,
                    failure_type="TAMPERED",
                    details=(f"Canonical hash mismatch for evidence '{ev.evidence_id.value}'."),
                )
                events.append(evt)
                self.audit_events.append(evt)
                return False, events

            if i > 0:
                prev_ev = evidences[i - 1]
                if ev.integrity.previous_hash != prev_ev.integrity.chain_hash:
                    evt = IntegrityFailureAuditEventDTO(
                        event_id=f"audit-chain-{ev.evidence_id.value}",
                        evidence_id=ev.evidence_id.value,
                        failure_type="CHAIN_BROKEN",
                        details=(f"Chain broken between turn {prev_ev.turn_id} and turn {ev.turn_id}."),
                    )
                    events.append(evt)
                    self.audit_events.append(evt)
                    return False, events

        return True, events
