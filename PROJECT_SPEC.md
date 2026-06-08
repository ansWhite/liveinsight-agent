# Multimodal RAG Shopping Guide Agent

## 1. Project Positioning

This project is a multimodal RAG-based ecommerce shopping guide Agent. It is designed to help users move from product search to purchase decision support by combining product knowledge ingestion, intent understanding, hybrid retrieval, multimodal parsing, streaming conversation, product card rendering, and evaluation feedback loops.

The system is not a thin LLM chatbot. The LLM is responsible for understanding, reasoning, and natural-language generation, while factual grounding comes from the product knowledge base, structured product database, retrieval evidence, and tool calls.

## 2. Core User Scenarios

1. Buying advice:
   - "I have a budget of 3000 RMB. Which phone has good camera quality and long battery life?"
2. Product comparison:
   - "What are the differences between these two air purifiers?"
3. Image-based shopping:
   - The user uploads a product image, packaging photo, poster, or screenshot and asks for identification or similar products.
4. Usage and suitability:
   - "Is this skincare product suitable for sensitive skin?"
5. Promotion decision:
   - "Which bundle is more cost-effective during the campaign?"
6. Follow-up conversation:
   - The Agent remembers user constraints such as budget, brand preference, use case, and contraindications.

## 3. Final Architecture

```text
iOS / Android / Web Client
  -> BFF / API Gateway
  -> Conversation Service
  -> Agent Orchestration Service
       -> Intent Router
       -> Context Manager
       -> Prompt Builder
       -> RAG Retriever
       -> Tool Executor
       -> Product Card Generator
       -> Answer Generator
  -> LLM Gateway
       -> OpenAI-compatible LLMs
       -> Multimodal models
       -> Embedding models
  -> Knowledge Services
       -> Document Ingestion
       -> OCR / Image Understanding
       -> Hybrid Retrieval
       -> Reranking
  -> Data Layer
       -> PostgreSQL
       -> Redis
       -> Qdrant / Milvus / pgvector
       -> OpenSearch / Elasticsearch
       -> MinIO / S3
  -> Evaluation and Observability
       -> Ragas
       -> promptfoo
       -> Langfuse / Phoenix
       -> OpenTelemetry
       -> Prometheus / Grafana
```

## 4. Recommended Technology Stack

### Client

- iOS: Swift, SwiftUI, Combine
- Android: Kotlin, Jetpack Compose, Coroutines
- Web demo: Next.js, React, TypeScript
- Streaming: SSE for token streaming, WebSocket for bidirectional interaction
- Local cache: CoreData, Room, or browser IndexedDB
- Image input: camera, gallery upload, compression, EXIF cleanup

### Backend

- BFF / API Gateway: NestJS, Go, or FastAPI for MVP
- Agent service: Python FastAPI
- Agent orchestration: LangGraph or OpenAI Agents SDK
- LLM gateway: LiteLLM or a self-built model gateway
- Async jobs: Celery, Dramatiq, Redis Streams, Kafka, or NATS
- Auth and rate limiting: JWT, API keys, Redis-based throttling

### RAG and Multimodal

- Vector database: Qdrant, Milvus, or pgvector
- Keyword search: OpenSearch or Elasticsearch
- Hybrid retrieval: BM25 + dense vector + structured filters
- Reranker: bge-reranker, cross-encoder, or commercial rerank API
- Embedding: bge-m3 or OpenAI-compatible embedding API
- OCR: Google ML Kit, PaddleOCR, or cloud OCR
- Image understanding: multimodal LLM or CLIP/SigLIP-style embedding model

### Data, Evaluation, and Observability

- Product database: PostgreSQL
- Cache and session state: Redis
- Object storage: MinIO, S3, or OSS
- Analytics: ClickHouse or Elasticsearch
- RAG evaluation: Ragas
- Prompt regression: promptfoo
- LLM tracing: Langfuse, Phoenix, or Helicone
- System tracing: OpenTelemetry
- Metrics: Prometheus and Grafana

## 5. Service Modules

### 5.1 Client App

Responsibilities:

- Render streaming AI responses.
- Insert product cards into the conversation stream.
- Upload text and images.
- Show product comparison views.
- Capture like/dislike and feedback.
- Keep session history and basic local cache.

Expected screens:

- Shopping guide chat page
- Product card detail sheet
- Product comparison page
- Image upload and recognition page
- Session history page
- Feedback entry

### 5.2 BFF / API Gateway

Responsibilities:

- User authentication and request validation.
- Client API aggregation.
- SSE/WebSocket connection management.
- Rate limiting and model usage quota control.
- Response schema adaptation for native clients.

### 5.3 Agent Orchestration Service

Responsibilities:

- Identify user intent.
- Manage multi-turn context.
- Rewrite and decompose queries.
- Select tools.
- Call RAG retrieval.
- Build prompts.
- Generate grounded answers.
- Generate product card schema.
- Apply fallback and safety strategies.

Suggested internal components:

- `IntentRouter`
- `ContextManager`
- `QueryRewriter`
- `RAGRetriever`
- `ToolExecutor`
- `PromptBuilder`
- `AnswerGenerator`
- `ProductCardGenerator`
- `SafetyGuard`

### 5.4 RAG Retrieval Service

Retrieval strategy:

1. Query rewrite based on user intent and conversation context.
2. Dense vector recall for semantic matching.
3. BM25 recall for brand, model, SKU, feature, and parameter matching.
4. Structured filtering by category, price, stock, rating, tags, and attributes.
5. Reranking with a cross-encoder or rerank model.
6. Context compression and citation packaging.

The Agent should answer with uncertainty when the retrieved evidence is insufficient.

### 5.5 Knowledge Ingestion Service

Supported sources:

- Product detail documents
- Marketing documents
- Campaign rules
- FAQ
- Reviews
- Product images and posters
- Manuals and comparison documents

Ingestion pipeline:

```text
Upload document/image
  -> Parse file
  -> Extract structured product fields
  -> Chunk text
  -> Generate embeddings
  -> Write chunks to vector DB
  -> Write searchable text to OpenSearch
  -> Write product attributes to PostgreSQL
  -> Store original files in MinIO/S3
```

### 5.6 Multimodal Parsing Service

Responsibilities:

- OCR product packaging, screenshots, posters, and manuals.
- Convert image content into text descriptions.
- Extract product names, brands, model numbers, prices, and visible attributes.
- Support image-to-product retrieval.
- Send parsed text into the same RAG flow as normal user queries.

### 5.7 Evaluation and Feedback System

Evaluation dimensions:

- Retrieval Recall@K
- Retrieval NDCG@K
- Context Precision
- Context Recall
- Answer Faithfulness
- Answer Relevance
- Product recommendation accuracy
- Multi-turn task completion rate
- First token latency
- End-to-end latency
- User satisfaction from feedback

Feedback loop:

```text
User feedback / offline eval failure
  -> Trace analysis
  -> Check retrieval evidence
  -> Update chunks, metadata, or product fields
  -> Tune prompt or reranker
  -> Run regression eval
  -> Release new prompt / knowledge version
```

## 6. Core API Design

### 6.1 Send Chat Message

```http
POST /api/v1/chat/messages
```

Request:

```json
{
  "session_id": "s_001",
  "user_id": "u_001",
  "message": "预算3000以内，拍照好一点的手机推荐哪个？",
  "image_url": null,
  "stream": true
}
```

Streaming event examples:

```json
{
  "type": "text_delta",
  "content": "根据你的预算和拍照需求，我建议优先看..."
}
```

```json
{
  "type": "product_card",
  "data": {
    "product_id": "p_001",
    "title": "Example Phone Pro",
    "price": 2899,
    "image_url": "https://example.com/p001.jpg",
    "reason": "主摄规格更强，夜景表现更好，价格符合预算"
  }
}
```

### 6.2 Upload Knowledge File

```http
POST /api/v1/knowledge/upload
```

Request:

```json
{
  "file_url": "s3://bucket/product-doc.pdf",
  "source_type": "product_doc",
  "product_id": "p_001"
}
```

### 6.3 Search Products

```http
POST /api/v1/products/search
```

Request:

```json
{
  "query": "3000以内 拍照好 续航强 手机",
  "filters": {
    "category": "phone",
    "max_price": 3000
  }
}
```

### 6.4 Submit Feedback

```http
POST /api/v1/feedback
```

Request:

```json
{
  "user_id": "u_001",
  "session_id": "s_001",
  "message_id": "m_001",
  "rating": "up",
  "comment": "推荐理由很清楚"
}
```

## 7. Core Data Model

### products

```text
id
title
brand
category
price
stock
rating
sales_count
main_image_url
tags
attributes_json
created_at
updated_at
```

### knowledge_chunks

```text
id
product_id
doc_id
chunk_text
chunk_type
source
embedding_id
metadata_json
created_at
```

### chat_sessions

```text
id
user_id
title
summary
created_at
updated_at
```

### chat_messages

```text
id
session_id
role
content
image_url
retrieval_trace_id
created_at
```

### retrieval_traces

```text
id
session_id
query
intent
retrieved_chunk_ids
reranked_chunk_ids
selected_product_ids
prompt_version
model_name
latency_ms
created_at
```

### feedbacks

```text
id
user_id
message_id
rating
feedback_type
comment
created_at
```

### eval_cases

```text
id
scenario
query
expected_answer
expected_products
golden_chunks
difficulty
created_at
```

## 8. Development Roadmap

### Phase 1: MVP RAG Chat

Goal:

Run through the minimum usable path: user question -> retrieval -> LLM -> streaming answer.

Tasks:

- Create FastAPI Agent service.
- Create PostgreSQL product schema.
- Create vector database collection.
- Implement document upload placeholder.
- Implement text chunking and embedding.
- Implement basic vector retrieval.
- Implement LLM answer generation.
- Implement SSE streaming endpoint.
- Create a simple web chat demo.

Acceptance criteria:

- A product document can be ingested.
- A user question can retrieve relevant chunks.
- The Agent can stream a grounded answer.
- The answer includes at least one citation or source reference.

### Phase 2: Product Decision Support

Goal:

Make the Agent recommend and compare products instead of only answering FAQs.

Tasks:

- Model structured product attributes.
- Implement product search and filtering.
- Implement product comparison tool.
- Implement product card schema.
- Generate recommendation reasons.
- Support budget, brand, use-case, and preference constraints.

Acceptance criteria:

- The Agent can recommend products under user constraints.
- The Agent can explain why one product is more suitable than another.
- Product cards are rendered in the client.

### Phase 3: Multi-turn Agent

Goal:

Support continuous decision-making conversations.

Tasks:

- Add session memory.
- Extract stable user preferences.
- Add query rewrite.
- Add intent routing.
- Add tool-call trace.
- Add fallback for insufficient evidence.

Acceptance criteria:

- The Agent remembers constraints across turns.
- The Agent asks clarifying questions when needed.
- Tool calls and retrieved evidence can be traced.

### Phase 4: Multimodal Input

Goal:

Support image-based shopping guide scenarios.

Tasks:

- Implement image upload.
- Add OCR.
- Add image understanding.
- Extract product candidates from images.
- Convert image understanding results into RAG queries.
- Support image-to-product retrieval.

Acceptance criteria:

- The user can upload a product image or screenshot.
- The Agent can identify visible product information.
- The Agent can recommend related or similar products.

### Phase 5: Evaluation and Feedback Loop

Goal:

Build interview-ready engineering credibility with measurable quality.

Tasks:

- Build 100 to 300 evaluation cases.
- Integrate Ragas.
- Integrate promptfoo.
- Save retrieval traces.
- Save prompt versions.
- Add user feedback collection.
- Create evaluation reports.

Acceptance criteria:

- The project reports retrieval Recall@K and NDCG@K.
- The project reports answer faithfulness and relevance.
- A failed case can be traced back to retrieval, prompt, or knowledge issues.

### Phase 6: Production Engineering

Goal:

Simulate a production-grade Agent system.

Tasks:

- Add LiteLLM model gateway.
- Add Redis cache.
- Add OpenTelemetry traces.
- Add Langfuse or Phoenix LLM observability.
- Add Docker Compose for local stack.
- Add rate limiting and authentication.
- Add prompt injection and sensitive-data guards.

Acceptance criteria:

- Services can be started locally with Docker Compose.
- Model calls, retrieval, and latency are observable.
- The system has basic safety and fallback behavior.

## 9. Suggested Repository Layout

```text
apps/
  api/                  FastAPI backend and Agent endpoints
  web/                  Next.js demo client
  ios/                  Optional SwiftUI native client
  android/              Optional Kotlin native client
packages/
  agent-core/           Intent, RAG, prompts, tools, evaluation modules
  shared-schemas/       Shared JSON schema and API contracts
data/
  samples/              Sample product docs, campaign docs, FAQs
  eval/                 Evaluation datasets
docs/
  architecture.md       System architecture
  product-requirements.md
  development-guide.md
  evaluation-guide.md
infra/
  docker-compose.yml
  qdrant/
  postgres/
  opensearch/
models/
  README.md             Model choices and fine-tuning notes
```

## 10. Interview Positioning

Recommended summary:

> This project is a multimodal RAG ecommerce shopping guide Agent. It is not just an LLM wrapper. I split the system into knowledge ingestion, intent understanding, hybrid retrieval, structured product decision support, streaming interaction, multimodal parsing, and evaluation feedback. The LLM handles reasoning and generation, while factual grounding is provided by RAG, product databases, retrieval traces, and tool calls.

Key talking points:

- Why hybrid retrieval is better than vector-only retrieval in ecommerce.
- How structured product filters reduce hallucination.
- How reranking improves evidence quality.
- How streaming and product card events improve client experience.
- How evaluation data drives prompt and knowledge base iteration.
- How model gateway, tracing, fallback, and safety make the system production-like.
