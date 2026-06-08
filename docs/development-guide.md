# Development Guide

## First Milestone

Build a working RAG shopping-guide loop:

```text
Product document
  -> chunking
  -> embedding
  -> vector storage
User question
  -> retrieval
  -> LLM answer
  -> streaming response
```

## Development Order

1. Finish backend health check.
2. Finish database connection.
3. Finish product seed data.
4. Finish document ingestion.
5. Finish vector retrieval.
6. Finish non-streaming chat.
7. Upgrade chat to SSE streaming.
8. Add product card event.
9. Add simple web UI.
10. Add evaluation script.

## MVP Done Criteria

- At least 10 products are in the database.
- Product documents can be ingested into the knowledge base.
- A user question retrieves relevant chunks.
- The Agent answers with evidence-grounded content.
- The client receives streaming text.
- The client can render at least one product card.
- A basic evaluation script reports retrieval hit rate.
