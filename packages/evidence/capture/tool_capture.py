"""Tool Capture Engine supporting Tool Intent and Tool Output (Item 7 Fix)."""

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


class ToolCaptureEngine:
    """Captures both Tool Intent Calls and Tool Execution Results."""

    def __init__(self, hasher: EvidenceHasherPort) -> None:
        self.hasher = hasher

    def capture_tool_call(
        self,
        evidence_id: str,
        user_id: str,
        session_id: str,
        turn_id: int,
        tool_name: str,
        arguments_json: str,
        previous_hash: str | None = None,
    ) -> Evidence:
        """Captures raw tool intent call as evidence."""
        ev_id = EvidenceId(value=evidence_id)
        meta = EvidenceMetadata.from_dict({"tool_name": tool_name})
        canon_hash, chain_hash = self.hasher.calculate_canonical_hash(
            evidence_id=evidence_id,
            evidence_type=EvidenceType.TOOL_CALL.value,
            user_id=user_id,
            session_id=session_id,
            turn_id=turn_id,
            raw_content=arguments_json,
            metadata_str=str(meta.entries),
            previous_hash=previous_hash,
        )

        content = EvidenceContent(
            raw_content=arguments_json,
            size_bytes=len(arguments_json.encode("utf-8")),
        )
        source = EvidenceSource(source_name=f"TOOL_CALL_{tool_name.upper()}", actor="AGENT")
        integrity = EvidenceIntegrityDTO(
            algorithm="SHA-256",
            canonical_hash=canon_hash,
            previous_hash=previous_hash,
            chain_hash=chain_hash,
            status=EvidenceStatus.CAPTURED,
        )

        return Evidence(
            evidence_id=ev_id,
            evidence_type=EvidenceType.TOOL_CALL,
            user_id=user_id,
            session_id=session_id,
            turn_id=turn_id,
            source=source,
            content=content,
            metadata=meta,
            integrity=integrity,
        )

    def capture_tool_result(
        self,
        evidence_id: str,
        user_id: str,
        session_id: str,
        turn_id: int,
        tool_name: str,
        tool_output: str,
        previous_hash: str | None = None,
    ) -> Evidence:
        """Captures raw tool execution output as evidence."""
        ev_id = EvidenceId(value=evidence_id)
        meta = EvidenceMetadata.from_dict({"tool_name": tool_name})
        canon_hash, chain_hash = self.hasher.calculate_canonical_hash(
            evidence_id=evidence_id,
            evidence_type=EvidenceType.TOOL_RESULT.value,
            user_id=user_id,
            session_id=session_id,
            turn_id=turn_id,
            raw_content=tool_output,
            metadata_str=str(meta.entries),
            previous_hash=previous_hash,
        )

        content = EvidenceContent(
            raw_content=tool_output,
            size_bytes=len(tool_output.encode("utf-8")),
        )
        source = EvidenceSource(source_name=f"TOOL_RESULT_{tool_name.upper()}", actor="SYSTEM")
        integrity = EvidenceIntegrityDTO(
            algorithm="SHA-256",
            canonical_hash=canon_hash,
            previous_hash=previous_hash,
            chain_hash=chain_hash,
            status=EvidenceStatus.CAPTURED,
        )

        return Evidence(
            evidence_id=ev_id,
            evidence_type=EvidenceType.TOOL_RESULT,
            user_id=user_id,
            session_id=session_id,
            turn_id=turn_id,
            source=source,
            content=content,
            metadata=meta,
            integrity=integrity,
        )
