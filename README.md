# LiveInsight Agent

LiveInsight Agent is a multimodal live-commerce analysis and content generation agent. It turns livestream videos, product documents, comments, danmaku, sales curves, and competitor materials into structured insights, highlight clips, replay reports, and short-video scripts.

## Core Architecture

- Multimodal parsing: video slicing, keyframes, ASR, OCR, visual summaries, timeline alignment.
- RAG knowledge layer: product documents, reviews, livestream transcripts, competitor data, multimodal segments.
- Multi-agent workflow: orchestration, video understanding, product RAG, data analysis, highlight detection, report generation, content generation.
- Model optimization: reranker fine-tuning, livestream segment LoRA, short-video script DPO, agent trajectory SFT.
- Business outputs: replay report, highlight clips, product selling points, user sentiment, competitor report, scripts, storyboard, subtitles.

## Repository Layout

```text
apps/
  api/                 FastAPI backend and async task entrypoints
  web/                 Next.js dashboard
packages/
  agent-core/          Agent, RAG, multimodal, training, and evaluation modules
infra/
  docker-compose.yml   Local PostgreSQL, Redis, MinIO, Qdrant stack
docs/
  architecture.md      System design and implementation plan
```

## Local Development

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

Infrastructure:

```bash
docker compose -f infra/docker-compose.yml up -d
```

## Interview Positioning

This project demonstrates an end-to-end large-model agent system: multimodal understanding, RAG, tool calling, multi-agent orchestration, structured output, async engineering, model fine-tuning, evaluation, and observability.
