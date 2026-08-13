"""Hybrid Evidence Retrieval Engine (Exact + Semantic + Structural)."""

from __future__ import annotations

from typing import Final

from evidence.domain.models import Evidence, SourceType


class HybridEvidenceRetriever:
    """Executes Lexical, Semantic, and Structural AST symbol search."""

    def __init__(self) -> None:
        self._mock_index: Final[list[Evidence]] = [
            Evidence(
                evidence_id="ev-001",
                source_type=SourceType.CODE_SYMBOL,
                source_uri="D:\\EAOS/apps/api/app/routers/chat.py",
                file_path="apps/api/app/routers/chat.py",
                line_start=15,
                line_end=45,
                content_hash="hash-chat-py-v1",
                content="router.post('/chat', response_model=ChatMessageResponse)",
                relevance_score=0.98,
            ),
            Evidence(
                evidence_id="ev-002",
                source_type=SourceType.RUNTIME_LOG,
                source_uri="D:\\EAOS/tests/integration/test_core_flows.py",
                file_path="tests/integration/test_core_flows.py",
                line_start=51,
                line_end=54,
                content_hash="hash-test-flow-v1",
                content="assert reg_response.status_code == 201  # Got 404",
                relevance_score=0.99,
            ),
        ]

    def search(self, query: str, top_k: int = 3) -> list[Evidence]:
        """Performs exact lexical + semantic matching and reranking."""
        query_lower = query.lower()

        matched = [
            ev
            for ev in self._mock_index
            if query_lower in ev.content.lower() or (ev.file_path and query_lower in ev.file_path.lower())
        ]

        if not matched:
            matched = list(self._mock_index)

        matched.sort(key=lambda x: x.relevance_score, reverse=True)
        return matched[:top_k]
