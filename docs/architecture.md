# Architecture

See `../PROJECT_SPEC.md` for the full architecture.

## MVP Architecture

```text
Web Demo
  -> FastAPI API
  -> Agent Core
  -> Retrieval
  -> LLM Gateway
  -> Streaming Response
```

## Production Target

```text
Native Apps / Web
  -> BFF
  -> Agent Service
  -> RAG Service
  -> Product Service
  -> Model Gateway
  -> Evaluation and Observability
```
