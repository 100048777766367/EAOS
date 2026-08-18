"""Chat WebSocket streaming evidence regression tests."""

from __future__ import annotations

import asyncio
from collections.abc import AsyncIterator
from pathlib import Path
from typing import Any

from apps.api.app.services.chat.orchestrator import ChatOrchestrator
from packages.evidence.domain.evidence_type import EvidenceType


class StubLLM:
    """Deterministic LLM stream for evidence tests."""

    async def generate_stream(
        self,
        messages: list[dict[str, Any]],
        temperature: float = 0.7,
        max_output_tokens: int = 4096,
        json_mode: bool = False,
    ) -> AsyncIterator[str]:
        yield "hello"
        yield " world"


class StubVerification:
    """Avoid invoking repository-wide verification in unit scope."""

    async def run(self) -> AsyncIterator[dict[str, Any]]:
        if False:
            yield {}


async def _collect_events(
    orchestrator: ChatOrchestrator,
) -> list[dict[str, Any]]:
    """Collect stream events from the async chat orchestrator."""
    return [
        event
        async for event in orchestrator.process_goal(
            conversation_id="conv-stream-evidence",
            message="Hello EAOS",
            system_instruction="",
            active_file="",
            temperature=0.1,
            max_output_tokens=16,
            json_mode=False,
        )
    ]


def test_chat_stream_records_user_and_assistant_evidence(
    tmp_path: Path,
) -> None:
    """Verify streaming chat persists both turns in the evidence ledger."""
    orchestrator = ChatOrchestrator(tmp_path)
    orchestrator.llm = StubLLM()
    orchestrator.verification = StubVerification()

    events = asyncio.run(
        _collect_events(orchestrator)
    )

    stream_start = events[0]
    stream_end = next(
        event for event in events if event["type"] == "stream_end"
    )
    response_complete = events[-1]

    assert stream_start["user_evidence_id"].startswith("E-")
    assert stream_end["assistant_evidence_id"].startswith("E-")
    assert response_complete["assistant_evidence_id"] == (
        stream_end["assistant_evidence_id"]
    )

    evidences = orchestrator.evidence.repo.list_by_session(
        "conv-stream-evidence"
    )
    assert [evidence.turn_id for evidence in evidences] == [1, 2]
    assert evidences[0].evidence_type is EvidenceType.USER_MESSAGE
    assert evidences[1].evidence_type is EvidenceType.ASSISTANT_MESSAGE
    assert evidences[0].content.raw_content == "Hello EAOS"
    assert evidences[1].content.raw_content == "hello world"
    assert evidences[1].integrity.previous_hash == (
        evidences[0].integrity.chain_hash
    )

    evidence_files = sorted(
        (tmp_path / ".memory" / "evidence_store").glob("E-*.json")
    )
    assert len(evidence_files) == 2
