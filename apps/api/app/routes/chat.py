import json

from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sse_starlette.sse import EventSourceResponse

from app.deps import get_rag_pipeline
from shopping_agent_core.rag_pipeline import RAGPipeline

router = APIRouter()


class ChatStreamRequest(BaseModel):
    session_id: str
    message: str
    image_url: str | None = None


@router.post("/stream")
async def stream_chat(
    request: ChatStreamRequest,
    pipeline: RAGPipeline = Depends(get_rag_pipeline),
) -> EventSourceResponse:
    async def events():
        async for event in pipeline.stream_answer(request.message):
            yield {"event": "message", "data": json.dumps(event, ensure_ascii=False)}
        yield {"event": "done", "data": "{}"}

    return EventSourceResponse(events())
