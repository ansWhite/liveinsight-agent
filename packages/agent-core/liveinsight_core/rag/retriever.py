from dataclasses import dataclass


@dataclass(frozen=True)
class RetrievalResult:
    text: str
    score: float
    source: str


class HybridRetriever:
    """Interface placeholder for dense + sparse retrieval with reranking."""

    def retrieve(self, query: str, top_k: int = 8) -> list[RetrievalResult]:
        return [
            RetrievalResult(
                text=f"Placeholder context for query: {query}",
                score=0.5,
                source="demo://hybrid-retriever",
            )
        ][:top_k]
