from qdrant_client import AsyncQdrantClient
from qdrant_client.models import Distance, PointStruct, VectorParams

from shopping_agent_core.schemas import ChunkRecord, RetrievalChunk

_VECTOR_DIM = 1024


class VectorStore:
    def __init__(self, url: str, api_key: str | None, collection: str) -> None:
        self._client = AsyncQdrantClient(url=url, api_key=api_key)
        self._collection = collection

    async def _ensure_collection(self) -> None:
        if not await self._client.collection_exists(self._collection):
            await self._client.create_collection(
                collection_name=self._collection,
                vectors_config=VectorParams(size=_VECTOR_DIM, distance=Distance.COSINE),
            )

    async def upsert(self, chunks: list[ChunkRecord], vectors: list[list[float]]) -> int:
        await self._ensure_collection()
        points = [
            PointStruct(
                id=chunk.chunk_id,
                vector=vector,
                payload={
                    "product_id": chunk.product_id,
                    "chunk_text": chunk.chunk_text,
                    "chunk_index": chunk.chunk_index,
                    "source": chunk.source,
                },
            )
            for chunk, vector in zip(chunks, vectors)
        ]
        await self._client.upsert(collection_name=self._collection, points=points)
        return len(points)

    async def search(self, query_vector: list[float], top_k: int = 5) -> list[RetrievalChunk]:
        results = await self._client.search(
            collection_name=self._collection,
            query_vector=query_vector,
            limit=top_k,
        )
        return [
            RetrievalChunk(
                chunk_id=str(r.id),
                product_id=r.payload.get("product_id"),
                text=r.payload.get("chunk_text", ""),
                score=r.score,
                source=r.payload.get("source"),
            )
            for r in results
        ]
