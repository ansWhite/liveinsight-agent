from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from shopping_agent_core.embedder import Embedder


@pytest.fixture
def embedder():
    return Embedder(
        api_key="test-key",
        base_url="https://api.siliconflow.cn/v1",
        model="BAAI/bge-m3",
    )


async def test_embed_returns_correct_shape(embedder):
    mock_item = MagicMock()
    mock_item.embedding = [0.1] * 1024
    mock_response = MagicMock()
    mock_response.data = [mock_item]

    with patch.object(embedder._client.embeddings, "create", new=AsyncMock(return_value=mock_response)):
        result = await embedder.embed(["hello world"])

    assert len(result) == 1
    assert len(result[0]) == 1024


async def test_embed_batches_at_32(embedder):
    mock_item = MagicMock()
    mock_item.embedding = [0.0] * 1024
    mock_response = MagicMock()
    mock_response.data = [mock_item] * 32

    calls = []

    async def fake_create(model, input):  # noqa: A002
        calls.append(len(input))
        mock_response.data = [mock_item] * len(input)
        return mock_response

    with patch.object(embedder._client.embeddings, "create", side_effect=fake_create):
        await embedder.embed(["text"] * 40)

    # 40 texts → first batch 32, second batch 8
    assert calls == [32, 8]


async def test_embed_multiple_texts(embedder):
    def make_response(n):
        r = MagicMock()
        r.data = [MagicMock(embedding=[float(i)] * 1024) for i in range(n)]
        return r

    with patch.object(
        embedder._client.embeddings,
        "create",
        new=AsyncMock(return_value=make_response(3)),
    ):
        result = await embedder.embed(["a", "b", "c"])

    assert len(result) == 3
