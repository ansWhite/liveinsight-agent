from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from shopping_agent_core.llm_client import LLMClient


@pytest.fixture
def client():
    return LLMClient(
        api_key="test-key",
        base_url="https://api.deepseek.com/v1",
        model="deepseek-chat",
    )


def _make_stream_chunk(content: str | None):
    chunk = MagicMock()
    chunk.choices = [MagicMock()]
    chunk.choices[0].delta.content = content
    return chunk


async def test_stream_chat_yields_tokens(client):
    chunks = [_make_stream_chunk("Hello"), _make_stream_chunk(" world"), _make_stream_chunk(None)]

    async def async_iter_chunks():
        for chunk in chunks:
            yield chunk

    mock_stream = async_iter_chunks()

    with patch.object(
        client._client.chat.completions,
        "create",
        new=AsyncMock(return_value=mock_stream),
    ):
        tokens = [t async for t in client.stream_chat([{"role": "user", "content": "hi"}])]

    assert tokens == ["Hello", " world"]


async def test_stream_chat_skips_none_content(client):
    chunks = [_make_stream_chunk(None), _make_stream_chunk("ok"), _make_stream_chunk(None)]

    async def async_iter_chunks():
        for chunk in chunks:
            yield chunk

    mock_stream = async_iter_chunks()

    with patch.object(
        client._client.chat.completions,
        "create",
        new=AsyncMock(return_value=mock_stream),
    ):
        tokens = [t async for t in client.stream_chat([{"role": "user", "content": "hi"}])]

    assert tokens == ["ok"]
