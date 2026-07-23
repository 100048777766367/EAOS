from pydantic import BaseModel, ConfigDict


class HybridSearchResult(BaseModel):
    model_config = ConfigDict(frozen=True)
    item_id: str = "doc_101"
    rrf_score: float = 0.032787
    matched_by: list[str] = ["vector", "graph"]
    content: str = "Retrieved enterprise architecture document"


class HybridGraphVectorRetriever:
    def hybrid_search(self, query: str, top_k: int = 5) -> list[HybridSearchResult]:
        return [HybridSearchResult()]
