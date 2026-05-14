# Implementation Plan

## Phase 1: MVP

- API project creation and upload registration
- Video parsing placeholder connected to a real file path
- ASR/OCR/keyframe task interfaces
- Simple report and highlight generation
- Dashboard page connected to backend routes

## Phase 2: RAG

- Product document ingestion
- Chunking and embedding
- Qdrant collection setup
- Hybrid retrieval and reranking interface
- Product RAG Agent

## Phase 3: Multi-Agent Workflow

- Replace deterministic scaffold with LangGraph
- Add typed tool interfaces
- Add trace persistence
- Add structured output validation
- Add retry and fallback policies

## Phase 4: Training

- Build reranker training dataset
- Build segment classification dataset
- Build script preference dataset
- Build agent trajectory dataset
- Add training scripts with PEFT, TRL, and FlagEmbedding

## Phase 5: Evaluation and Demo

- RAG Recall@K and NDCG@10
- Highlight Top-K hit rate
- Script preference win rate
- Agent tool-call success rate
- Demo video and interview-ready README
