"""Conversation Capture Engine depending purely on Ports (Item 6 Fix)."""

from __future__ import annotations

from packages.evidence.domain.evidence import Evidence
from packages.evidence.domain.evidence_content import EvidenceContent
from packages.evidence.domain.evidence_id import EvidenceId
from packages.evidence.domain.evidence_integrity import (
    EvidenceIntegrityDTO,
)
from packages.evidence.domain.evidence_metadata import EvidenceMetadata
from packages.evidence.domain.evidence_source import EvidenceSource
from packages.evidence.domain.evidence_status import EvidenceStatus
from packages.evidence.domain.evidence_type import EvidenceType
from packages.evidence.ports.evidence_hasher import EvidenceHasherPort


class ConversationCaptureEngine:
    """Captures conversation turns into raw evidence records via Hasher Port."""

    def __init__(self, hasher: EvidenceHasherPort) -> None:
        self.hasher = hasher

    def capture_turn(
        self,
        evidence_id: str,
        user_id: str,
        session_id: str,
        turn_id: int,
        raw_text: str,
        role: str = "USER",
        previous_hash: str | None = None,
    ) -> Evidence:
        """Captures conversation turn as raw evidence with canonical chain."""
        ev_id = EvidenceId(value=evidence_id)
        ev_type = EvidenceType.USER_MESSAGE if role.upper() == "USER" else EvidenceType.ASSISTANT_MESSAGE
        meta = EvidenceMetadata.from_dict({"role": role})

        canon_hash, chain_hash = self.hasher.calculate_canonical_hash(
            evidence_id=evidence_id,
            evidence_type=ev_type.value,
            user_id=user_id,
            session_id=session_id,
            turn_id=turn_id,
            raw_content=raw_text,
            metadata_str=str(meta.entries),
            previous_hash=previous_hash,
        )

        content = EvidenceContent(
            raw_content=raw_text,
            size_bytes=len(raw_text.encode("utf-8")),
        )
        source = EvidenceSource(source_name=role.upper(), actor=user_id)
        integrity = EvidenceIntegrityDTO(
            algorithm="SHA-256",
            canonical_hash=canon_hash,
            previous_hash=previous_hash,
            chain_hash=chain_hash,
            status=EvidenceStatus.CAPTURED,
        )

        return Evidence(
            evidence_id=ev_id,
            evidence_type=ev_type,
            user_id=user_id,
            session_id=session_id,
            turn_id=turn_id,
            source=source,
            content=content,
            metadata=meta,
            integrity=integrity,
        )
