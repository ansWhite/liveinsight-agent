# Phase 1 Real RAG Pipeline Design

Date: 2026-06-11

## Goal

Replace the current rule-based demo in `apps/api/app/routes/chat.py` with a real RAG pipeline:
document ingest → chunking → embedding → Qdrant vector storage → retrieval → LLM streaming generation.

Phase 2 (structured product search, product comparison) follows after Phase 1 is verified end-to-end.

## Tech Stack Decisions

| Component | Choice | Reason |
|-----------|--------|--------|
| LLM | DeepSeek via OpenAI-compatible API | User has existing key |
| Embedding | SiliconFlow bge-m3 | Free tier, strong Chinese support, OpenAI-compatible |
| Vector DB | Qdrant Cloud (free tier) | No Docker required, 1GB sufficient for portfolio |
| Chunking | Paragraph split + sentence boundary fallback | Simple, auditable, good for product docs |

## Environment Variables (new additions to `.env`)

```env
# LLM
OPENAI_API_KEY=sk-xxx
OPENAI_BASE_URL=https://api.deepseek.com/v1
LLM_MODEL=deepseek-chat

# Embedding
SILICONFLOW_API_KEY=sk-xxx
EMBEDDING_BASE_URL=https://api.siliconflow.cn/v1
EMBEDDING_MODEL=BAAI/bge-m3

# Qdrant Cloud
QDRANT_URL=https://xxx.qdrant.io
QDRANT_API_KEY=xxx
QDRANT_COLLECTION=product_knowledge
```

## File Changes

### New files in `packages/agent-core/shopping_agent_core/`

**`chunker.py`**
- `split(content: str, source: str, product_id: str) -> list[ChunkRecord]`
- Split on `\n\n` paragraph boundaries
- If a paragraph exceeds 500 characters, split further at sentence boundaries (`. ` / `。`)
- Overlap: each chunk prepends the last sentence of the previous paragraph
- Returns `ChunkRecord(chunk_id, product_id, source, chunk_text, chunk_index)`

**`embedder.py`**
- `embed(texts: list[str]) -> list[list[float]]`
- Calls SiliconFlow `/v1/embeddings` with model `BAAI/bge-m3`
- Batches requests at 32 texts per call
- Returns list of 1024-dimensional float vectors

**`vectorstore.py`**
- `upsert(chunks: list[ChunkRecord], vectors: list[list[float]]) -> int`
- `search(query_vector: list[float], top_k: int = 5) -> list[RetrievalChunk]`
- Wraps Qdrant Python SDK, targets Qdrant Cloud
- Collection created on first upsert if it does not exist (dimension=1024, cosine distance)
- Point ID: deterministic UUID from `product_id + chunk_index`

**`retriever.py`**
- `retrieve(query: str, top_k: int = 5) -> list[RetrievalChunk]`
- Calls `embedder.embed([query])` then `vectorstore.search(vector, top_k)`
- Returns `RetrievalChunk` list (already defined in `schemas.py`)

**`llm_client.py`**
- `stream_chat(messages: list[dict]) -> AsyncIterator[str]`
- Calls DeepSeek (or any OpenAI-compatible) via `openai.AsyncOpenAI(base_url=..., api_key=...)`
- Yields token strings from the streaming response

**`rag_pipeline.py`**
- `build_prompt(chunks: list[RetrievalChunk], user_message: str) -> list[dict]`
  - System: `SHOPPING_GUIDE_SYSTEM_PROMPT`
  - Injects retrieved chunks as a numbered context block
  - If chunks is empty, adds instruction: "No product knowledge retrieved. Tell the user honestly."
- `stream_answer(user_message: str) -> AsyncIterator[dict]`
  - Calls `retriever.retrieve(user_message)`
  - Calls `build_prompt(chunks, user_message)`
  - Streams LLM tokens as `{"type": "text_delta", "content": token}`
  - After stream ends, emits one `{"type": "product_card", "data": {...}}` per unique `product_id` in chunks
  - Reads product card data from `data/samples/products.json` (Phase 2 replaces with PostgreSQL)

### Modified files

**`apps/api/app/routes/knowledge.py`**
- Replace placeholder with real pipeline: `chunker.split → embedder.embed → vectorstore.upsert`
- Return actual `chunks_created` count

**`apps/api/app/routes/chat.py`**
- Replace `demo_chat_events` with `rag_pipeline.stream_answer`
- Keep `ChatStreamRequest` schema unchanged (SSE protocol unchanged)

**`apps/api/app/config.py`**
- Add `siliconflow_api_key`, `embedding_base_url`, `embedding_model`, `qdrant_api_key`

## Data Flow

### Knowledge Ingest

```
POST /api/v1/knowledge/ingest
  { product_id, title, content }
  → chunker.split(content, source=title, product_id)
  → embedder.embed([chunk.chunk_text for chunk in chunks])
  → vectorstore.upsert(chunks, vectors)
  ← { status: "ok", product_id, chunks_created: N }
```

### Chat Stream

```
POST /api/v1/chat/stream
  { session_id, message }
  → retriever.retrieve(message, top_k=5)
  → rag_pipeline.build_prompt(chunks, message)
  → llm_client.stream_chat(messages)
  ← SSE: text_delta × N
  ← SSE: product_card (one per retrieved product)
  ← SSE: done
```

## Qdrant Point Schema

```
id:      UUID (deterministic from product_id + chunk_index)
vector:  float[1024]
payload:
  product_id:   str
  chunk_text:   str
  chunk_index:  int
  source:       str
```

## Error Handling

| Failure | Behavior |
|---------|----------|
| Embedding API error | `knowledge/ingest` returns 500 with error detail |
| Qdrant upsert error | `knowledge/ingest` returns 500 with error detail |
| Zero retrieval results | RAG proceeds; prompt instructs LLM to answer honestly without fabricating |
| LLM stream error | SSE emits `text_delta` with apology message; stream closes |

## Verification Plan

1. Ingest `data/samples/product_doc_p_demo_001.md` via `POST /knowledge/ingest`
2. Confirm chunks are visible in Qdrant Cloud dashboard
3. Send `POST /chat/stream` with "预算3000，拍照好的手机"
4. Confirm SSE stream returns real LLM text (not rule-based) and a product_card event
5. Send a query unrelated to any ingested product (e.g., "推荐一款空气净化器")
6. Confirm LLM answers honestly that no relevant product was found

## Out of Scope for Phase 1

- BM25 keyword search (Phase 3)
- Multi-turn session memory (Phase 3)
- Image upload / OCR (Phase 4)
- PostgreSQL product database (Phase 2)
- Evaluation metrics (Phase 5)
