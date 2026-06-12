import json
from unittest.mock import AsyncMock, MagicMock

import pytest
from fastapi.testclient import TestClient

from app.deps import get_rag_pipeline
from app.main import app


def make_pipeline(ingest_count=2, stream_events=None):
    if stream_events is None:
        stream_events = [
            {"type": "text_delta", "content": "好的"},
            {"type": "product_card", "data": {"product_id": "p001", "title": "Phone", "price": 2899, "image_url": "", "reason": "test"}},
        ]

    async def fake_stream(message):
        for event in stream_events:
            yield event

    p = MagicMock()
    p.ingest = AsyncMock(return_value=ingest_count)
    p.stream_answer = fake_stream
    return p


@pytest.fixture(autouse=True)
def override_pipeline():
    mock = make_pipeline()
    app.dependency_overrides[get_rag_pipeline] = lambda: mock
    yield mock
    app.dependency_overrides.clear()


@pytest.fixture
def client():
    return TestClient(app)


def test_ingest_returns_chunks_created(client, override_pipeline):
    override_pipeline.ingest = AsyncMock(return_value=3)
    response = client.post(
        "/api/v1/knowledge/ingest",
        json={"product_id": "p001", "title": "Test Doc", "content": "Para one.\n\nPara two.\n\nPara three."},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ok"
    assert data["chunks_created"] == 3


def test_chat_stream_returns_sse(client):
    response = client.post(
        "/api/v1/chat/stream",
        json={"session_id": "s1", "message": "推荐手机"},
    )
    assert response.status_code == 200
    assert "text/event-stream" in response.headers["content-type"]
    body = response.text
    assert "text_delta" in body
    assert "product_card" in body
