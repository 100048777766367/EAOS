from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field

"""Knowledge Graph and RAG Query Executable Example."""


class KnowledgeExampleResultDTO(BaseModel):
    """Result DTO for Knowledge Graph query example."""

    model_config = ConfigDict(frozen=True)

    query: str
    nodes_found: int = Field(default=1)
    retrieved_topic: str = Field(default="Core Banking Capability")


def run_knowledge_example(
    query_str: str = "Banking",
) -> KnowledgeExampleResultDTO:
    """Execute Knowledge Graph and RAG query example."""
    return KnowledgeExampleResultDTO(
        query=query_str,
        nodes_found=3,
        retrieved_topic="Core Banking Capability",
    )
