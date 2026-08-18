"""Chat orchestrator for EAOS AI Studio."""

from __future__ import annotations

from collections.abc import AsyncGenerator
from pathlib import Path
from typing import Any
from uuid import uuid4

from apps.api.app.adapters.llm.gemini import GeminiAdapter
from apps.api.app.services.chat.context_manager import ContextManager
from apps.api.app.services.chat.conversation_store import ConversationStore
from apps.api.app.services.chat.verification.coordinator import (
    VerificationCoordinator,
)
from packages.evidence.enterprise_evidence import (
    EAOSEnterpriseEvidencePackageEngine,
)


class ChatOrchestrator:
    """Coordinate context, LLM streaming, and verification."""

    def __init__(self, project_root: Path) -> None:
        """Initialize chat services."""
        self.store = ConversationStore()
        self.context_mgr = ContextManager(project_root)
        self.llm = GeminiAdapter()
        self.verification = VerificationCoordinator(project_root)
        self.evidence = EAOSEnterpriseEvidencePackageEngine(project_root)

    def _record_message_evidence(
        self,
        conversation_id: str,
        role: str,
        content: str,
        turn_id: int,
    ) -> str:
        """Persist one chat message into the append-only evidence ledger."""
        evidence_id = f"E-{uuid4().hex}"
        evidence = self.evidence.record_turn_evidence(
            evidence_id=evidence_id,
            user_id=conversation_id,
            session_id=conversation_id,
            turn_id=turn_id,
            content=content,
            role=role,
        )
        return evidence.evidence_id.value

    async def process_goal(
        self,
        conversation_id: str,
        message: str,
        system_instruction: str,
        active_file: str,
        temperature: float,
        max_output_tokens: int,
        json_mode: bool,
    ) -> AsyncGenerator[dict[str, Any], None]:
        """Process one chat request."""
        self.store.add_message(
            conversation_id,
            "user",
            message,
        )
        user_turn_id = len(self.store.get_history(conversation_id))
        user_evidence_id = self._record_message_evidence(
            conversation_id=conversation_id,
            role="USER",
            content=message,
            turn_id=user_turn_id,
        )

        file_ctx = self.context_mgr.build_file_context(
            active_file,
        )

        full_system = "\n\n".join(
            part
            for part in (
                system_instruction,
                file_ctx,
            )
            if part.strip()
        )

        history = self.store.get_history(conversation_id)

        messages: list[dict[str, Any]] = []

        if full_system:
            messages.append(
                {
                    "role": "system",
                    "content": full_system,
                }
            )

        messages.extend(
            {
                "role": item.role,
                "content": item.content,
            }
            for item in history
            if item.role != "system"
        )

        yield {
            "type": "stream_start",
            "message": "LLM stream started",
            "user_evidence_id": user_evidence_id,
        }

        full_response = ""
        chunk_count = 0

        try:
            async for token in self.llm.generate_stream(
                messages=messages,
                temperature=temperature,
                max_output_tokens=max_output_tokens,
                json_mode=json_mode,
            ):
                chunk_count += 1
                full_response += token

                yield {
                    "type": "stream_chunk",
                    "content": token,
                    "index": chunk_count,
                }

        except Exception as exc:
            yield {
                "type": "stream_error",
                "error": str(exc),
            }
            raise

        if not full_response:
            raise RuntimeError(
                "LLM returned an empty response.",
            )

        self.store.add_message(
            conversation_id,
            "assistant",
            full_response,
        )
        assistant_turn_id = len(self.store.get_history(conversation_id))
        assistant_evidence_id = self._record_message_evidence(
            conversation_id=conversation_id,
            role="ASSISTANT",
            content=full_response,
            turn_id=assistant_turn_id,
        )

        yield {
            "type": "stream_end",
            "reply": full_response,
            "chunks": chunk_count,
            "assistant_evidence_id": assistant_evidence_id,
        }

        yield {
            "type": "response_complete",
            "reply": full_response,
            "assistant_evidence_id": assistant_evidence_id,
        }

        async for event in self.verification.run():
            yield event
