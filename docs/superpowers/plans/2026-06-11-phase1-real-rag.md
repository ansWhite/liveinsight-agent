# Phase 1 Real RAG Pipeline Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Replace the rule-based demo in `apps/api` with a real RAG pipeline: knowledge ingest → chunking → embedding (SiliconFlow bge-m3) → Qdrant Cloud vector storage → retrieval → DeepSeek LLM streaming generation.

**Architecture:** New modules in `packages/agent-core/shopping_agent_core/` implement pure domain logic (chunker, embedder, vectorstore, retriever, llm_client, rag_pipeline). A new `apps/api/app/deps.py` wires those modules with settings from `.env`. FastAPI routes delegate to `RAGPipeline` via `Depends()`.

**Tech Stack:** Python 3.11+, FastAPI, openai SDK 1.58.1 (for both LLM and embedding), qdrant-client 1.12.1, pytest 8.x + pytest-asyncio 0.24.x.

---

## File Map

| Action | Path | Responsibility |
|--------|------|---------------|
| Modify | `apps/api/requirements.txt` | Add pytest, pytest-asyncio |
| Modify | `apps/api/app/config.py` | Add siliconflow_api_key, embedding_base_url, qdrant_api_key |
| Modify | `.env.example` | Document new env vars |
| Create | `apps/api/pytest.ini` | Set asyncio_mode = auto |
| Create | `apps/api/tests/__init__.py` | Empty, marks test package |
| Modify | `packages/agent-core/shopping_agent_core/schemas.py` | Add ChunkRecord |
| Create | `packages/agent-core/shopping_agent_core/chunker.py` | Paragraph split with overlap |
| Create | `packages/agent-core/shopping_agent_core/embedder.py` | SiliconFlow bge-m3 client |
| Create | `packages/agent-core/shopping_agent_core/vectorstore.py` | Qdrant Cloud read/write |
| Create | `packages/agent-core/shopping_agent_core/retriever.py` | embed query → vector search |
| Create | `packages/agent-core/shopping_agent_core/llm_client.py` | DeepSeek streaming chat |
| Create | `packages/agent-core/shopping_agent_core/rag_pipeline.py` | ingest + stream_answer |
| Create | `apps/api/app/deps.py` | Singleton factory for RAGPipeline |
| Modify | `apps/api/app/routes/knowledge.py` | Real ingest via pipeline |
| Modify | `apps/api/app/routes/chat.py` | Real RAG via pipeline |
| Create | `apps/api/tests/test_chunker.py` | Unit tests |
| Create | `apps/api/tests/test_embedder.py` | Mocked HTTP tests |
| Create | `apps/api/tests/test_vectorstore.py` | In-memory Qdrant tests |
| Create | `apps/api/tests/test_retriever.py` | Mocked component tests |
| Create | `apps/api/tests/test_llm_client.py` | Mocked OpenAI tests |
| Create | `apps/api/tests/test_rag_pipeline.py` | Mocked pipeline tests |
| Create | `apps/api/tests/test_routes.py` | FastAPI TestClient tests |

---

## Task 1: Setup — dependencies, config, pytest

**Files:**
- Modify: `apps/api/requirements.txt`
- Modify: `apps/api/app/config.py`
- Modify: `.env.example`
- Create: `apps/api/pytest.ini`
- Create: `apps/api/tests/__init__.py`

- [ ] **Step 1: Add test dependencies to requirements.txt**

Append to `apps/api/requirements.txt`:
```
pytest==8.3.4
pytest-asyncio==0.24.0
httpx==0.28.1
```
(httpx is already there — keep the existing line, just add the two pytest lines)

- [ ] **Step 2: Add new settings to config.py**

Replace the entire `apps/api/app/config.py` with:
```python
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_env: str = "local"
    app_name: str = "shopping-guide-agent"

    # Qdrant Cloud
    qdrant_url: str = "http://localhost:6333"
    qdrant_api_key: str | None = None
    qdrant_collection: str = "product_knowledge"

    # LLM (DeepSeek or any OpenAI-compatible)
    openai_api_key: str | None = None
    openai_base_url: str | None = None
    llm_model: str = "deepseek-chat"

    # Embedding (SiliconFlow bge-m3)
    siliconflow_api_key: str | None = None
    embedding_base_url: str = "https://api.siliconflow.cn/v1"
    embedding_model: str = "BAAI/bge-m3"

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


settings = Settings()
```

- [ ] **Step 3: Update .env.example**

Replace `.env.example` with:
```
# App
APP_ENV=local
APP_NAME=shopping-guide-agent

# LLM (DeepSeek or any OpenAI-compatible endpoint)
OPENAI_API_KEY=sk-xxx
OPENAI_BASE_URL=https://api.deepseek.com/v1
LLM_MODEL=deepseek-chat

# Embedding (SiliconFlow bge-m3)
SILICONFLOW_API_KEY=sk-xxx
EMBEDDING_BASE_URL=https://api.siliconflow.cn/v1
EMBEDDING_MODEL=BAAI/bge-m3

# Qdrant Cloud
QDRANT_URL=https://xxx.qdrant.io
QDRANT_API_KEY=xxx
QDRANT_COLLECTION=product_knowledge
```

- [ ] **Step 4: Create pytest.ini**

Create `apps/api/pytest.ini`:
```ini
[pytest]
asyncio_mode = auto
testpaths = tests
```

- [ ] **Step 5: Create tests/__init__.py**

Create `apps/api/tests/__init__.py` as an empty file.

- [ ] **Step 6: Install agent-core package into the venv**

Run from `apps/api/`:
```bash
.venv\Scripts\pip install -e ..\..\packages\agent-core
```

Expected output: `Successfully installed shopping-guide-agent-core-0.1.0`

- [ ] **Step 7: Install new test dependencies**

Run from `apps/api/`:
```bash
.venv\Scripts\pip install pytest==8.3.4 pytest-asyncio==0.24.0
```

Expected output: `Successfully installed pytest-... pytest-asyncio-...`

- [ ] **Step 8: Smoke-test pytest**

Run from `apps/api/`:
```bash
.venv\Scripts\pytest --collect-only
```

Expected output: `no tests ran` (no errors)

- [ ] **Step 9: Commit**

```bash
git add apps/api/requirements.txt apps/api/app/config.py .env.example apps/api/pytest.ini apps/api/tests/__init__.py
git commit -m "chore: add pytest setup and new config fields for real RAG"
```

---

## Task 2: ChunkRecord schema + Chunker

**Files:**
- Modify: `packages/agent-core/shopping_agent_core/schemas.py`
- Create: `packages/agent-core/shopping_agent_core/chunker.py`
- Create: `apps/api/tests/test_chunker.py`

- [ ] **Step 1: Write the failing tests**

Create `apps/api/tests/test_chunker.py`:
```python
from shopping_agent_core.chunker import split


def test_split_creates_one_chunk_per_paragraph():
    content = "Para one.\n\nPara two.\n\nPara three."
    chunks = split(content, source="Test Doc", product_id="p001")
    assert len(chunks) == 3


def test_split_chunk_metadata():
    chunks = split("Only paragraph.", source="My Doc", product_id="p_abc")
    assert chunks[0].product_id == "p_abc"
    assert chunks[0].source == "My Doc"
    assert chunks[0].chunk_index == 0


def test_split_long_paragraph_is_broken_down():
    # Single paragraph longer than 500 chars must be split
    long_para = ("This is a long sentence. " * 25).strip()  # ~625 chars
    chunks = split(long_para, source="Test", product_id="p001")
    assert len(chunks) > 1
    for chunk in chunks:
        assert len(chunk.chunk_text) <= 600  # allow small overflow at sentence boundary


def test_split_overlap_includes_last_sentence_of_previous():
    content = "First sentence. Second sentence.\n\nThird sentence."
    chunks = split(content, source="Test", product_id="p001")
    # Second chunk should contain the last sentence of the first paragraph
    assert "Second sentence." in chunks[1].chunk_text
    assert "Third sentence." in chunks[1].chunk_text


def test_split_chunk_ids_are_unique():
    content = "Para one.\n\nPara two.\n\nPara three."
    chunks = split(content, source="Test", product_id="p001")
    ids = [c.chunk_id for c in chunks]
    assert len(ids) == len(set(ids))


def test_split_empty_content_returns_empty():
    assert split("", source="Test", product_id="p001") == []


def test_split_ignores_blank_only_paragraphs():
    content = "Para one.\n\n   \n\nPara two."
    chunks = split(content, source="Test", product_id="p001")
    assert len(chunks) == 2
```

- [ ] **Step 2: Run tests — confirm they fail**

```bash
cd apps/api && .venv\Scripts\pytest tests/test_chunker.py -v
```

Expected: `ImportError` or `ModuleNotFoundError` for `shopping_agent_core.chunker`

- [ ] **Step 3: Add ChunkRecord to schemas.py**

Append to `packages/agent-core/shopping_agent_core/schemas.py`:
```python


class ChunkRecord(BaseModel):
    """Internal record produced by the chunker before embedding and storage."""

    chunk_id: str
    product_id: str
    source: str
    chunk_text: str
    chunk_index: int
```

- [ ] **Step 4: Create chunker.py**

Create `packages/agent-core/shopping_agent_core/chunker.py`:
```python
import re
import uuid

from shopping_agent_core.schemas import ChunkRecord

_MAX_CHARS = 500


def _chunk_id(product_id: str, index: int) -> str:
    return str(uuid.uuid5(uuid.NAMESPACE_OID, f"{product_id}:{index}"))


def _split_long(text: str, max_chars: int) -> list[str]:
    sentences = re.split(r"(?<=[.。!?！？])\s+", text)
    parts: list[str] = []
    current = ""
    for sentence in sentences:
        if current and len(current) + 1 + len(sentence) > max_chars:
            parts.append(current)
            current = sentence
        else:
            current = (current + " " + sentence).strip() if current else sentence
    if current:
        parts.append(current)
    return parts or [text]


def split(
    content: str,
    source: str,
    product_id: str,
    max_chars: int = _MAX_CHARS,
) -> list[ChunkRecord]:
    if not content.strip():
        return []

    paragraphs = [p.strip() for p in re.split(r"\n\n+", content) if p.strip()]

    raw: list[str] = []
    for para in paragraphs:
        if len(para) <= max_chars:
            raw.append(para)
        else:
            raw.extend(_split_long(para, max_chars))

    # Overlap: prepend last sentence of previous raw chunk
    with_overlap: list[str] = []
    for i, chunk in enumerate(raw):
        if i == 0:
            with_overlap.append(chunk)
        else:
            prev_sentences = re.split(r"(?<=[.。!?！？])\s+", raw[i - 1])
            overlap = prev_sentences[-1] if prev_sentences else ""
            with_overlap.append((overlap + " " + chunk).strip() if overlap else chunk)

    return [
        ChunkRecord(
            chunk_id=_chunk_id(product_id, i),
            product_id=product_id,
            source=source,
            chunk_text=text,
            chunk_index=i,
        )
        for i, text in enumerate(with_overlap)
    ]
```

- [ ] **Step 5: Run tests — confirm they pass**

```bash
cd apps/api && .venv\Scripts\pytest tests/test_chunker.py -v
```

Expected: all 7 tests `PASSED`

- [ ] **Step 6: Commit**

```bash
git add packages/agent-core/shopping_agent_core/schemas.py packages/agent-core/shopping_agent_core/chunker.py apps/api/tests/test_chunker.py
git commit -m "feat: add ChunkRecord schema and paragraph chunker with overlap"
```

---

## Task 3: Embedder

**Files:**
- Create: `packages/agent-core/shopping_agent_core/embedder.py`
- Create: `apps/api/tests/test_embedder.py`

- [ ] **Step 1: Write the failing tests**

Create `apps/api/tests/test_embedder.py`:
```python
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
```

- [ ] **Step 2: Run tests — confirm they fail**

```bash
cd apps/api && .venv\Scripts\pytest tests/test_embedder.py -v
```

Expected: `ImportError` for `shopping_agent_core.embedder`

- [ ] **Step 3: Create embedder.py**

Create `packages/agent-core/shopping_agent_core/embedder.py`:
```python
from openai import AsyncOpenAI

_BATCH_SIZE = 32


class Embedder:
    def __init__(self, api_key: str, base_url: str, model: str) -> None:
        self._client = AsyncOpenAI(api_key=api_key, base_url=base_url)
        self._model = model

    async def embed(self, texts: list[str]) -> list[list[float]]:
        all_vectors: list[list[float]] = []
        for i in range(0, len(texts), _BATCH_SIZE):
            batch = texts[i : i + _BATCH_SIZE]
            response = await self._client.embeddings.create(
                model=self._model,
                input=batch,
            )
            all_vectors.extend(item.embedding for item in response.data)
        return all_vectors
```

- [ ] **Step 4: Run tests — confirm they pass**

```bash
cd apps/api && .venv\Scripts\pytest tests/test_embedder.py -v
```

Expected: all 3 tests `PASSED`

- [ ] **Step 5: Commit**

```bash
git add packages/agent-core/shopping_agent_core/embedder.py apps/api/tests/test_embedder.py
git commit -m "feat: add Embedder using SiliconFlow bge-m3 via OpenAI SDK"
```

---

## Task 4: VectorStore

**Files:**
- Create: `packages/agent-core/shopping_agent_core/vectorstore.py`
- Create: `apps/api/tests/test_vectorstore.py`

- [ ] **Step 1: Write the failing tests**

Create `apps/api/tests/test_vectorstore.py`:
```python
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
    # Should not raise even though collection doesn't exist yet
    await store.upsert([chunk], [[0.1] * 1024])
    exists = await store._client.collection_exists(store._collection)
    assert exists
```

- [ ] **Step 2: Run tests — confirm they fail**

```bash
cd apps/api && .venv\Scripts\pytest tests/test_vectorstore.py -v
```

Expected: `ImportError` for `shopping_agent_core.vectorstore`

- [ ] **Step 3: Create vectorstore.py**

Create `packages/agent-core/shopping_agent_core/vectorstore.py`:
```python
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
```

- [ ] **Step 4: Run tests — confirm they pass**

```bash
cd apps/api && .venv\Scripts\pytest tests/test_vectorstore.py -v
```

Expected: all 4 tests `PASSED`

- [ ] **Step 5: Commit**

```bash
git add packages/agent-core/shopping_agent_core/vectorstore.py apps/api/tests/test_vectorstore.py
git commit -m "feat: add VectorStore with Qdrant Cloud upsert and cosine search"
```

---

## Task 5: Retriever

**Files:**
- Create: `packages/agent-core/shopping_agent_core/retriever.py`
- Create: `apps/api/tests/test_retriever.py`

- [ ] **Step 1: Write the failing tests**

Create `apps/api/tests/test_retriever.py`:
```python
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
```

- [ ] **Step 2: Run tests — confirm they fail**

```bash
cd apps/api && .venv\Scripts\pytest tests/test_retriever.py -v
```

Expected: `ImportError` for `shopping_agent_core.retriever`

- [ ] **Step 3: Create retriever.py**

Create `packages/agent-core/shopping_agent_core/retriever.py`:
```python
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
```

- [ ] **Step 4: Run tests — confirm they pass**

```bash
cd apps/api && .venv\Scripts\pytest tests/test_retriever.py -v
```

Expected: all 2 tests `PASSED`

- [ ] **Step 5: Commit**

```bash
git add packages/agent-core/shopping_agent_core/retriever.py apps/api/tests/test_retriever.py
git commit -m "feat: add Retriever composing Embedder and VectorStore"
```

---

## Task 6: LLM Client

**Files:**
- Create: `packages/agent-core/shopping_agent_core/llm_client.py`
- Create: `apps/api/tests/test_llm_client.py`

- [ ] **Step 1: Write the failing tests**

Create `apps/api/tests/test_llm_client.py`:
```python
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
    mock_stream = AsyncMock()
    mock_stream.__aiter__ = MagicMock(return_value=iter(chunks))

    with patch.object(
        client._client.chat.completions,
        "create",
        new=AsyncMock(return_value=mock_stream),
    ):
        tokens = [t async for t in client.stream_chat([{"role": "user", "content": "hi"}])]

    assert tokens == ["Hello", " world"]


async def test_stream_chat_skips_none_content(client):
    chunks = [_make_stream_chunk(None), _make_stream_chunk("ok"), _make_stream_chunk(None)]
    mock_stream = AsyncMock()
    mock_stream.__aiter__ = MagicMock(return_value=iter(chunks))

    with patch.object(
        client._client.chat.completions,
        "create",
        new=AsyncMock(return_value=mock_stream),
    ):
        tokens = [t async for t in client.stream_chat([{"role": "user", "content": "hi"}])]

    assert tokens == ["ok"]
```

- [ ] **Step 2: Run tests — confirm they fail**

```bash
cd apps/api && .venv\Scripts\pytest tests/test_llm_client.py -v
```

Expected: `ImportError` for `shopping_agent_core.llm_client`

- [ ] **Step 3: Create llm_client.py**

Create `packages/agent-core/shopping_agent_core/llm_client.py`:
```python
from collections.abc import AsyncIterator

from openai import AsyncOpenAI


class LLMClient:
    def __init__(self, api_key: str, base_url: str, model: str) -> None:
        self._client = AsyncOpenAI(api_key=api_key, base_url=base_url)
        self._model = model

    async def stream_chat(self, messages: list[dict]) -> AsyncIterator[str]:
        stream = await self._client.chat.completions.create(
            model=self._model,
            messages=messages,
            stream=True,
        )
        async for chunk in stream:
            token = chunk.choices[0].delta.content
            if token:
                yield token
```

- [ ] **Step 4: Run tests — confirm they pass**

```bash
cd apps/api && .venv\Scripts\pytest tests/test_llm_client.py -v
```

Expected: all 2 tests `PASSED`

- [ ] **Step 5: Commit**

```bash
git add packages/agent-core/shopping_agent_core/llm_client.py apps/api/tests/test_llm_client.py
git commit -m "feat: add LLMClient for DeepSeek streaming chat via OpenAI SDK"
```

---

## Task 7: RAG Pipeline

**Files:**
- Create: `packages/agent-core/shopping_agent_core/rag_pipeline.py`
- Create: `apps/api/tests/test_rag_pipeline.py`

- [ ] **Step 1: Write the failing tests**

Create `apps/api/tests/test_rag_pipeline.py`:
```python
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
```

- [ ] **Step 2: Run tests — confirm they fail**

```bash
cd apps/api && .venv\Scripts\pytest tests/test_rag_pipeline.py -v
```

Expected: `ImportError` for `shopping_agent_core.rag_pipeline`

- [ ] **Step 3: Create rag_pipeline.py**

Create `packages/agent-core/shopping_agent_core/rag_pipeline.py`:
```python
import json
from collections.abc import AsyncIterator
from pathlib import Path

from shopping_agent_core.chunker import split as chunk_split
from shopping_agent_core.llm_client import LLMClient
from shopping_agent_core.prompts import SHOPPING_GUIDE_SYSTEM_PROMPT
from shopping_agent_core.retriever import Retriever
from shopping_agent_core.schemas import RetrievalChunk


class RAGPipeline:
    def __init__(
        self,
        retriever: Retriever,
        llm_client: LLMClient,
        products_file: Path | None = None,
    ) -> None:
        self._retriever = retriever
        self._llm_client = llm_client
        self._products_file = products_file

    async def ingest(self, product_id: str, title: str, content: str) -> int:
        chunks = chunk_split(content, source=title, product_id=product_id)
        vectors = await self._retriever.embedder.embed([c.chunk_text for c in chunks])
        return await self._retriever.vectorstore.upsert(chunks, vectors)

    def _build_messages(self, chunks: list[RetrievalChunk], user_message: str) -> list[dict]:
        if chunks:
            context_lines = [
                f"[{i + 1}] {c.source or 'unknown'}\n{c.text}"
                for i, c in enumerate(chunks)
            ]
            system = SHOPPING_GUIDE_SYSTEM_PROMPT + "\n\nProduct knowledge:\n" + "\n\n".join(context_lines)
        else:
            system = (
                SHOPPING_GUIDE_SYSTEM_PROMPT
                + "\n\nNo product knowledge was retrieved. "
                "Tell the user honestly that you don't have relevant product information."
            )
        return [
            {"role": "system", "content": system},
            {"role": "user", "content": user_message},
        ]

    def _load_product_cards(self, product_ids: list[str]) -> list[dict]:
        if not self._products_file or not self._products_file.exists():
            return []
        products: list[dict] = json.loads(self._products_file.read_text(encoding="utf-8"))
        seen: set[str] = set()
        cards: list[dict] = []
        for pid in product_ids:
            if pid in seen:
                continue
            seen.add(pid)
            for p in products:
                if p["id"] == pid:
                    cards.append(
                        {
                            "product_id": p["id"],
                            "title": p["title"],
                            "price": p.get("price"),
                            "image_url": p.get("main_image_url", ""),
                            "reason": "Based on retrieved product knowledge.",
                        }
                    )
        return cards

    async def stream_answer(self, user_message: str) -> AsyncIterator[dict]:
        chunks = await self._retriever.retrieve(user_message, top_k=5)
        messages = self._build_messages(chunks, user_message)

        async for token in self._llm_client.stream_chat(messages):
            yield {"type": "text_delta", "content": token}

        product_ids = [c.product_id for c in chunks if c.product_id]
        for card in self._load_product_cards(product_ids):
            yield {"type": "product_card", "data": card}
```

- [ ] **Step 4: Run tests — confirm they pass**

```bash
cd apps/api && .venv\Scripts\pytest tests/test_rag_pipeline.py -v
```

Expected: all 4 tests `PASSED`

- [ ] **Step 5: Commit**

```bash
git add packages/agent-core/shopping_agent_core/rag_pipeline.py apps/api/tests/test_rag_pipeline.py
git commit -m "feat: add RAGPipeline with ingest and streaming answer generation"
```

---

## Task 8: deps.py + route updates

**Files:**
- Create: `apps/api/app/deps.py`
- Modify: `apps/api/app/routes/knowledge.py`
- Modify: `apps/api/app/routes/chat.py`
- Create: `apps/api/tests/test_routes.py`

- [ ] **Step 1: Write the failing route tests**

Create `apps/api/tests/test_routes.py`:
```python
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
```

- [ ] **Step 2: Run tests — confirm they fail**

```bash
cd apps/api && .venv\Scripts\pytest tests/test_routes.py -v
```

Expected: `ImportError` for `app.deps`

- [ ] **Step 3: Create deps.py**

Create `apps/api/app/deps.py`:
```python
from functools import cache
from pathlib import Path

from shopping_agent_core.embedder import Embedder
from shopping_agent_core.llm_client import LLMClient
from shopping_agent_core.rag_pipeline import RAGPipeline
from shopping_agent_core.retriever import Retriever
from shopping_agent_core.vectorstore import VectorStore

from app.config import settings

_PRODUCTS_FILE = Path(__file__).resolve().parents[3] / "data" / "samples" / "products.json"


@cache
def get_rag_pipeline() -> RAGPipeline:
    embedder = Embedder(
        api_key=settings.siliconflow_api_key or "",
        base_url=settings.embedding_base_url,
        model=settings.embedding_model,
    )
    vectorstore = VectorStore(
        url=settings.qdrant_url,
        api_key=settings.qdrant_api_key,
        collection=settings.qdrant_collection,
    )
    retriever = Retriever(embedder=embedder, vectorstore=vectorstore)
    llm_client = LLMClient(
        api_key=settings.openai_api_key or "",
        base_url=settings.openai_base_url or "https://api.deepseek.com/v1",
        model=settings.llm_model,
    )
    return RAGPipeline(
        retriever=retriever,
        llm_client=llm_client,
        products_file=_PRODUCTS_FILE,
    )
```

- [ ] **Step 4: Update knowledge.py**

Replace `apps/api/app/routes/knowledge.py` with:
```python
from fastapi import APIRouter, Depends
from pydantic import BaseModel

from app.deps import get_rag_pipeline
from shopping_agent_core.rag_pipeline import RAGPipeline

router = APIRouter()


class KnowledgeIngestRequest(BaseModel):
    product_id: str
    title: str
    content: str


@router.post("/ingest")
async def ingest_knowledge(
    request: KnowledgeIngestRequest,
    pipeline: RAGPipeline = Depends(get_rag_pipeline),
) -> dict[str, object]:
    count = await pipeline.ingest(request.product_id, request.title, request.content)
    return {
        "status": "ok",
        "product_id": request.product_id,
        "title": request.title,
        "chunks_created": count,
    }
```

- [ ] **Step 5: Update chat.py**

Replace `apps/api/app/routes/chat.py` with:
```python
import json

from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sse_starlette.sse import EventSourceResponse

from app.deps import get_rag_pipeline
from shopping_agent_core.rag_pipeline import RAGPipeline

router = APIRouter()


class ChatStreamRequest(BaseModel):
    session_id: str
    message: str
    image_url: str | None = None


@router.post("/stream")
async def stream_chat(
    request: ChatStreamRequest,
    pipeline: RAGPipeline = Depends(get_rag_pipeline),
) -> EventSourceResponse:
    async def events():
        async for event in pipeline.stream_answer(request.message):
            yield {"event": "message", "data": json.dumps(event, ensure_ascii=False)}
        yield {"event": "done", "data": "{}"}

    return EventSourceResponse(events())
```

- [ ] **Step 6: Run all tests — confirm they pass**

```bash
cd apps/api && .venv\Scripts\pytest -v
```

Expected: all tests `PASSED`, no errors

- [ ] **Step 7: Commit**

```bash
git add apps/api/app/deps.py apps/api/app/routes/knowledge.py apps/api/app/routes/chat.py apps/api/tests/test_routes.py
git commit -m "feat: wire RAGPipeline into knowledge and chat routes via FastAPI Depends"
```

---

## Task 9: End-to-end manual verification

**Prerequisites:** `.env` file exists with real `SILICONFLOW_API_KEY`, `OPENAI_API_KEY`, `OPENAI_BASE_URL`, `QDRANT_URL`, `QDRANT_API_KEY` set.

- [ ] **Step 1: Create .env from example**

Copy `.env.example` to `.env` and fill in the real values:
```
OPENAI_API_KEY=<DeepSeek key>
OPENAI_BASE_URL=https://api.deepseek.com/v1
LLM_MODEL=deepseek-chat
SILICONFLOW_API_KEY=<SiliconFlow key>
EMBEDDING_BASE_URL=https://api.siliconflow.cn/v1
EMBEDDING_MODEL=BAAI/bge-m3
QDRANT_URL=<Qdrant Cloud cluster URL>
QDRANT_API_KEY=<Qdrant Cloud API key>
QDRANT_COLLECTION=product_knowledge
```

- [ ] **Step 2: Start the API**

```bash
cd apps/api && .venv\Scripts\uvicorn app.main:app --reload
```

Expected: `Application startup complete.` (port 8000)

- [ ] **Step 3: Ingest the sample product document**

Read content of `data/samples/product_doc_p_demo_001.md` and POST:
```bash
curl -X POST http://localhost:8000/api/v1/knowledge/ingest \
  -H "Content-Type: application/json" \
  -d "{\"product_id\": \"p_demo_001\", \"title\": \"Demo Phone Pro\", \"content\": \"$(cat ../../data/samples/product_doc_p_demo_001.md)\"}"
```

On Windows PowerShell:
```powershell
$content = Get-Content "..\..\data\samples\product_doc_p_demo_001.md" -Raw
$body = @{product_id="p_demo_001"; title="Demo Phone Pro"; content=$content} | ConvertTo-Json
Invoke-RestMethod -Method Post -Uri "http://localhost:8000/api/v1/knowledge/ingest" -ContentType "application/json" -Body $body
```

Expected response: `{"status":"ok","product_id":"p_demo_001","chunks_created":4}`  
(exact count may vary by 1–2 depending on overlap logic)

- [ ] **Step 4: Confirm chunks visible in Qdrant Cloud dashboard**

Open `https://cloud.qdrant.io` → your cluster → Collections → `product_knowledge`.
Expected: collection exists with 4–6 points.

- [ ] **Step 5: Test a relevant query**

```powershell
$body = @{session_id="s1"; message="预算3000以内，拍照好的手机推荐哪个？"} | ConvertTo-Json
Invoke-RestMethod -Method Post -Uri "http://localhost:8000/api/v1/chat/stream" -ContentType "application/json" -Body $body
```

Expected: streaming SSE text containing real LLM-generated recommendation (not the old rule-based string), followed by a `product_card` event for `p_demo_001`.

- [ ] **Step 6: Test an irrelevant query**

```powershell
$body = @{session_id="s2"; message="推荐一款空气净化器"} | ConvertTo-Json
Invoke-RestMethod -Method Post -Uri "http://localhost:8000/api/v1/chat/stream" -ContentType "application/json" -Body $body
```

Expected: LLM responds honestly that no relevant product was found; no `product_card` event (or one that doesn't match air purifiers).

- [ ] **Step 7: Final commit**

```bash
git add .env.example
git commit -m "feat: Phase 1 real RAG pipeline complete — ingest, retrieve, stream"
```

---

## Self-Review Checklist

- [x] All spec sections have corresponding tasks
- [x] No TBDs or placeholder steps
- [x] Type names consistent across tasks (`ChunkRecord`, `RetrievalChunk`, `RAGPipeline`, `Retriever`, `Embedder`, `VectorStore`, `LLMClient`)
- [x] Method signatures consistent: `Retriever.retrieve(query, top_k)`, `RAGPipeline.ingest(product_id, title, content)`, `RAGPipeline.stream_answer(user_message)`
- [x] All imports reference modules defined in this plan
- [x] `.env` is in `.gitignore` (already was)
