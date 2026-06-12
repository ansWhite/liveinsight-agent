from shopping_agent_core.embedder import Embedder
from shopping_agent_core.schemas import RetrievalChunk
from shopping_agent_core.vectorstore import VectorStore


class Retriever:
    def __init__(self, embedder: Embedder, vectorstore: VectorStore) -> None:
        self.embedder = embedder
        self.vectorstore = vectorstore

    async def retrieve(self, query: str, top_k: int = 5) -> list[RetrievalChunk]:
        vectors = await self.embedder.embed([query])
        return await self.vectorstore.search(vectors[0], top_k=top_k)
