import pytest
from qdrant_client import AsyncQdrantClient

from shopping_agent_core.schemas import ChunkRecord
from shopping_agent_core.vectorstore import VectorStore


@pytest.fixture
async def store():
    client = AsyncQdrantClient(location=":memory:")
    vs = VectorStore.__new__(VectorStore)
    vs._client = client
    vs._collection = "test_col"
    return vs


async def test_upsert_returns_count(store):
    chunk = ChunkRecord(
        chunk_id="00000000-0000-0000-0000-000000000001",
        product_id="p001",
        source="Test",
        chunk_text="test text",
        chunk_index=0,
    )
    count = await store.upsert([chunk], [[0.1] * 1024])
    assert count == 1


async def test_search_returns_matching_chunk(store):
    chunk = ChunkRecord(
        chunk_id="00000000-0000-0000-0000-000000000002",
        product_id="p002",
        source="Test Source",
        chunk_text="camera and battery",
        chunk_index=0,
    )
    vector = [0.5] * 1024
    await store.upsert([chunk], [vector])

    results = await store.search(vector, top_k=1)

    assert len(results) == 1
    assert results[0].product_id == "p002"
    assert results[0].text == "camera and battery"
    assert results[0].source == "Test Source"
    assert 0.0 <= results[0].score <= 1.0


async def test_search_respects_top_k(store):
    chunks = [
        ChunkRecord(
            chunk_id=f"00000000-0000-0000-0000-00000000000{i}",
            product_id="p001",
            source="Test",
            chunk_text=f"chunk {i}",
            chunk_index=i,
        )
        for i in range(1, 6)
    ]
    vectors = [[float(i) / 10] * 1024 for i in range(1, 6)]
    await store.upsert(chunks, vectors)

    results = await store.search([0.1] * 1024, top_k=2)
    assert len(results) == 2


async def test_collection_created_automatically(store):
    chunk = ChunkRecord(
        chunk_id="00000000-0000-0000-0000-000000000009",
        product_id="p001",
        source="Test",
        chunk_text="auto create",
        chunk_index=0,
    )
    await store.upsert([chunk], [[0.1] * 1024])
    exists = await store._client.collection_exists(store._collection)
    assert exists
