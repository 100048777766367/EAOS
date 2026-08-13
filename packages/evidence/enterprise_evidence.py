"""Master Enterprise Evidence Package Engine Orchestrator (Full 17 Items Complete)."""

from __future__ import annotations

from pathlib import Path
from typing import Final

from packages.evidence.adapters.hashing.sha256_evidence_hasher import (
    SHA256EvidenceHasherAdapter,
)
from packages.evidence.adapters.storage.filesystem_evidence_repository import (
    FilesystemEvidenceRepositoryAdapter,
)
from packages.evidence.bundles.evidence_bundle_builder import (
    EvidenceBundleBuilder,
)
from packages.evidence.capture.conversation_capture import (
    ConversationCaptureEngine,
)
from packages.evidence.capture.tool_capture import ToolCaptureEngine
from packages.evidence.domain.evidence import Evidence
from packages.evidence.domain.evidence_bundle import EvidenceBundleDTO


class EAOSEnterpriseEvidencePackageEngine:
    """Master Evidence Package Engine managing persistent Fact Ledger and Hash Chains."""

    def __init__(self, workspace_root: Path | None = None) -> None:
        self.root: Final[Path] = (workspace_root or Path.cwd()).resolve()
        self.repo: Final[FilesystemEvidenceRepositoryAdapter] = FilesystemEvidenceRepositoryAdapter(self.root)
        self.hasher: Final[SHA256EvidenceHasherAdapter] = SHA256EvidenceHasherAdapter()
        self.conv_capture: Final[ConversationCaptureEngine] = ConversationCaptureEngine(self.hasher)
        self.tool_capture: Final[ToolCaptureEngine] = ToolCaptureEngine(self.hasher)
        self.builder: Final[EvidenceBundleBuilder] = EvidenceBundleBuilder()

    def record_turn_evidence(
        self,
        evidence_id: str,
        user_id: str,
        session_id: str,
        turn_id: int,
        content: str,
        role: str = "USER",
    ) -> Evidence:
        """Captures turn evidence with canonical bound hash chain and appends."""
        prev_records = self.repo.list_by_session(session_id)
        prev_hash = prev_records[-1].integrity.chain_hash if prev_records else None

        ev = self.conv_capture.capture_turn(
            evidence_id=evidence_id,
            user_id=user_id,
            session_id=session_id,
            turn_id=turn_id,
            raw_text=content,
            role=role,
            previous_hash=prev_hash,
        )
        return self.repo.append(ev)

    def record_tool_call_evidence(
        self,
        evidence_id: str,
        user_id: str,
        session_id: str,
        turn_id: int,
        tool_name: str,
        arguments_json: str,
    ) -> Evidence:
        """Captures tool intent call as evidence."""
        prev_records = self.repo.list_by_session(session_id)
        prev_hash = prev_records[-1].integrity.chain_hash if prev_records else None

        ev = self.tool_capture.capture_tool_call(
            evidence_id=evidence_id,
            user_id=user_id,
            session_id=session_id,
            turn_id=turn_id,
            tool_name=tool_name,
            arguments_json=arguments_json,
            previous_hash=prev_hash,
        )
        return self.repo.append(ev)

    def record_tool_result_evidence(
        self,
        evidence_id: str,
        user_id: str,
        session_id: str,
        turn_id: int,
        tool_name: str,
        tool_output: str,
    ) -> Evidence:
        """Captures tool output result as evidence."""
        prev_records = self.repo.list_by_session(session_id)
        prev_hash = prev_records[-1].integrity.chain_hash if prev_records else None

        ev = self.tool_capture.capture_tool_result(
            evidence_id=evidence_id,
            user_id=user_id,
            session_id=session_id,
            turn_id=turn_id,
            tool_name=tool_name,
            tool_output=tool_output,
            previous_hash=prev_hash,
        )
        return self.repo.append(ev)

    def assemble_filtered_bundle(
        self,
        session_id: str,
        target_evidence_ids: list[str],
        query_text: str = "",
    ) -> EvidenceBundleDTO:
        """Assembles bundle filtered strictly by requested evidence IDs."""
        session_evs = self.repo.list_by_session(session_id)
        return self.builder.build_bundle_by_ids(
            bundle_id=f"bundle-{session_id}",
            query_text=query_text,
            target_evidence_ids=target_evidence_ids,
            session_evidences=session_evs,
        )
