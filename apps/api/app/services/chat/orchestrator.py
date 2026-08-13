"""Chat orchestrator for EAOS AI Studio."""

from __future__ import annotations

from collections.abc import AsyncGenerator
from pathlib import Path
from typing import Any

from apps.api.app.adapters.llm.gemini import GeminiAdapter
from apps.api.app.services.chat.context_manager import ContextManager
from apps.api.app.services.chat.conversation_store import ConversationStore
from apps.api.app.services.chat.verification.coordinator import (
    VerificationCoordinator,
)


class ChatOrchestrator:
    """Coordinate context, LLM streaming, and verification."""

    def __init__(self, project_root: Path) -> None:
        """Initialize chat services."""
        self.store = ConversationStore()
        self.context_mgr = ContextManager(project_root)
        self.llm = GeminiAdapter()
        self.verification = VerificationCoordinator(project_root)

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

        yield {
            "type": "stream_end",
            "reply": full_response,
            "chunks": chunk_count,
        }

        yield {
            "type": "response_complete",
            "reply": full_response,
        }

        async for event in self.verification.run():
            yield event
