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
