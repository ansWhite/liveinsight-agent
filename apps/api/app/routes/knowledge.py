from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter()


class KnowledgeIngestRequest(BaseModel):
    product_id: str
    title: str
    content: str


@router.post("/ingest")
async def ingest_knowledge(request: KnowledgeIngestRequest) -> dict[str, object]:
    return {
        "status": "accepted",
        "product_id": request.product_id,
        "title": request.title,
        "chunks_created": 0,
    }
