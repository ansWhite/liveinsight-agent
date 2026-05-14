# LiveInsight Agent Architecture

## Goal

Build a multimodal live-commerce agent that analyzes livestream replays and related business data, then generates actionable replay reports, highlight clips, product insights, competitor analysis, and short-video scripts.

## High-Level Flow

```text
Upload video/product/comments/metrics
  -> API and task queue
  -> Multimodal parsing
  -> Structured timeline
  -> RAG indexing
  -> Multi-agent workflow
  -> Reports, clips, scripts, and next-session strategy
```

## Layers

1. Frontend dashboard
   - Project upload
   - Video timeline
   - Agent trace
   - Report and script editor

2. Backend API
   - Project lifecycle
   - Upload orchestration
   - Async analysis job status
   - Chat and report endpoints

3. Multimodal parsing
   - FFmpeg video slicing
   - ASR transcript generation
   - OCR extraction
   - Keyframe and visual summary generation
   - Comment and sales timeline alignment

4. RAG knowledge layer
   - Product documents
   - Reviews and comments
   - Livestream transcript segments
   - Competitor documents
   - Multimodal segment summaries

5. Agent workflow
   - Orchestrator Agent
   - Video Understanding Agent
   - Product RAG Agent
   - Data Analysis Agent
   - Highlight Detection Agent
   - Report Agent
   - Content Generation Agent
   - Competitor Analysis Agent

6. Model optimization
   - Domain reranker fine-tuning for RAG
   - LoRA segment classifier for livestream intent and highlight pre-filtering
   - DPO for short-video script quality
   - Agent trajectory SFT for tool-selection behavior

7. Evaluation
   - ASR WER
   - OCR accuracy
   - RAG Recall@K and NDCG@10
   - Highlight Top-K hit rate
   - Tool-call success rate
   - Report factuality
   - Script preference win rate

## MVP Scope

The first usable version should support:

- Upload one livestream video.
- Upload one product markdown or text document.
- Upload optional comments and sales metrics CSV files.
- Generate ASR/OCR/keyframe segment records.
- Index product and segment text into vector search.
- Run a multi-agent analysis workflow.
- Output a replay report, highlight list, and three short-video script drafts.
