import json
from pathlib import Path
from unittest.mock import AsyncMock, MagicMock

import pytest

from shopping_agent_core.rag_pipeline import RAGPipeline
from shopping_agent_core.schemas import RetrievalChunk


def make_retriever(chunks: list[RetrievalChunk]):
    r = AsyncMock()
    r.retrieve = AsyncMock(return_value=chunks)
    r.embedder = AsyncMock()
    r.vectorstore = AsyncMock()
    r.vectorstore.upsert = AsyncMock(return_value=len(chunks))
    return r


def make_llm_client(tokens: list[str]):
    async def fake_stream(messages):
        for t in tokens:
            yield t

    c = MagicMock()
    c.stream_chat = fake_stream
    return c


@pytest.fixture
def products_file(tmp_path: Path) -> Path:
    data = [{"id": "p001", "title": "Demo Phone Pro", "price": 2899}]
    f = tmp_path / "products.json"
    f.write_text(json.dumps(data), encoding="utf-8")
    return f


async def test_stream_answer_yields_text_deltas(products_file):
    retriever = make_retriever(
        [RetrievalChunk(chunk_id="c1", product_id="p001", text="great camera", score=0.9, source="Doc")]
    )
    llm = make_llm_client(["推荐", "这款", "手机"])
    pipeline = RAGPipeline(retriever=retriever, llm_client=llm, products_file=products_file)

    events = [e async for e in pipeline.stream_answer("推荐手机")]

    text_events = [e for e in events if e["type"] == "text_delta"]
    assert len(text_events) == 3
    assert text_events[0]["content"] == "推荐"


async def test_stream_answer_yields_product_card(products_file):
    retriever = make_retriever(
        [RetrievalChunk(chunk_id="c1", product_id="p001", text="great camera", score=0.9, source="Doc")]
    )
    llm = make_llm_client(["ok"])
    pipeline = RAGPipeline(retriever=retriever, llm_client=llm, products_file=products_file)

    events = [e async for e in pipeline.stream_answer("推荐手机")]

    card_events = [e for e in events if e["type"] == "product_card"]
    assert len(card_events) == 1
    assert card_events[0]["data"]["product_id"] == "p001"
    assert card_events[0]["data"]["title"] == "Demo Phone Pro"


async def test_stream_answer_no_chunks_no_product_card(products_file):
    retriever = make_retriever([])
    llm = make_llm_client(["抱歉，没有找到相关商品。"])
    pipeline = RAGPipeline(retriever=retriever, llm_client=llm, products_file=products_file)

    events = [e async for e in pipeline.stream_answer("未知商品")]

    card_events = [e for e in events if e["type"] == "product_card"]
    assert card_events == []


async def test_ingest_calls_embedder_and_vectorstore(products_file):
    retriever = make_retriever([])
    retriever.embedder.embed = AsyncMock(return_value=[[0.1] * 1024] * 3)
    retriever.vectorstore.upsert = AsyncMock(return_value=3)
    llm = make_llm_client([])
    pipeline = RAGPipeline(retriever=retriever, llm_client=llm, products_file=products_file)

    count = await pipeline.ingest("p001", "Demo Doc", "Para one.\n\nPara two.\n\nPara three.")

    assert count == 3
    retriever.embedder.embed.assert_called_once()
    retriever.vectorstore.upsert.assert_called_once()
