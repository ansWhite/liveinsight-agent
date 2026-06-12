from unittest.mock import AsyncMock

import pytest

from shopping_agent_core.retriever import Retriever
from shopping_agent_core.schemas import RetrievalChunk


@pytest.fixture
def mock_embedder():
    e = AsyncMock()
    e.embed = AsyncMock(return_value=[[0.1] * 1024])
    return e


@pytest.fixture
def mock_vectorstore():
    vs = AsyncMock()
    vs.search = AsyncMock(
        return_value=[
            RetrievalChunk(
                chunk_id="abc",
                product_id="p001",
                text="good camera phone",
                score=0.92,
                source="Demo Doc",
            )
        ]
    )
    return vs


async def test_retrieve_embeds_query_and_searches(mock_embedder, mock_vectorstore):
    retriever = Retriever(embedder=mock_embedder, vectorstore=mock_vectorstore)
    results = await retriever.retrieve("camera phone", top_k=3)

    mock_embedder.embed.assert_called_once_with(["camera phone"])
    mock_vectorstore.search.assert_called_once_with([0.1] * 1024, top_k=3)
    assert len(results) == 1
    assert results[0].product_id == "p001"


async def test_retrieve_returns_empty_when_no_results(mock_embedder, mock_vectorstore):
    mock_vectorstore.search.return_value = []
    retriever = Retriever(embedder=mock_embedder, vectorstore=mock_vectorstore)
    results = await retriever.retrieve("unknown product")
    assert results == []
