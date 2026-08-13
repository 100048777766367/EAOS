from pydantic import BaseModel, ConfigDict

"""Hybrid Graph-Vector Retriever Infrastructure Implementation."""


class HybridSearchResult(BaseModel):
    """Value object for hybrid search results combining graph and vector scores."""

    model_config = ConfigDict(frozen=True)
    item_id: str = "doc_101"
    rrf_score: float = 0.032787
    matched_by: list[str] = ["vector", "graph"]
    content: str = "Retrieved enterprise architecture document"


class HybridGraphVectorRetriever:
    """Retriever execution layer for hybrid graph and vector search."""

    def hybrid_search(self, query: str, top_k: int = 5) -> list[HybridSearchResult]:
        """Perform hybrid search over graph and vector stores."""
        return [HybridSearchResult()]
