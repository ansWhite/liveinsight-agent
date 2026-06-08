# Multimodal RAG Shopping Guide Agent

An ecommerce shopping guide Agent built around multimodal input, RAG retrieval, structured product decision support, streaming interaction, and evaluation feedback loops.

The project goal is to demonstrate a production-style Agent system for interview and practical development scenarios. It is not just a chatbot wrapper: product facts are grounded by RAG, structured product data, retrieval traces, and tool calls.

## Core Capabilities

- Product document ingestion and knowledge-base construction
- Hybrid retrieval with vector search, keyword search, and structured filters
- RAG-based grounded answers
- Multi-turn shopping intent understanding
- Streaming chat responses
- Product card schema generation
- Text and image input parsing
- Product recommendation and comparison
- Evaluation and feedback loop
- Observability for model calls, retrieval, latency, and cost

## Repository Layout

```text
apps/
  api/                  FastAPI backend and Agent endpoints
  web/                  Next.js demo client
packages/
  agent-core/           Intent, RAG, prompts, tools, and evaluation modules
  shared-schemas/       Shared API and event schemas
data/
  samples/              Sample products and product documents
  eval/                 Evaluation datasets
docs/
  architecture.md       System architecture
  development-guide.md  Practical development guide
  product-requirements.md
  evaluation-guide.md
infra/
  docker-compose.yml    Local PostgreSQL, Redis, Qdrant, MinIO stack
models/
  README.md             Model choices and tuning notes
```

## Local Development

Infrastructure:

```bash
docker compose -f infra/docker-compose.yml up -d
```

Backend:

```bash
cd apps/api
python -m venv .venv
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Frontend:

```bash
cd apps/web
npm install
npm run dev
```

## First Milestone

Build the MVP loop:

```text
Product document -> chunking -> embedding -> retrieval -> LLM -> streaming answer
```

See `PROJECT_SPEC.md` for the full system design.
