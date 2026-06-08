import asyncio
import json
from collections.abc import AsyncIterator

from fastapi import APIRouter
from pydantic import BaseModel
from sse_starlette.sse import EventSourceResponse

router = APIRouter()


class ChatStreamRequest(BaseModel):
    session_id: str
    message: str
    image_url: str | None = None


async def demo_chat_events(request: ChatStreamRequest) -> AsyncIterator[dict[str, str]]:
    text = (
        "我会先结合你的预算、使用场景和商品知识库做检索，"
        "再给出推荐理由和可对比的商品卡片。"
    )
    for char in text:
        yield {
            "event": "message",
            "data": json.dumps({"type": "text_delta", "content": char}, ensure_ascii=False),
        }
        await asyncio.sleep(0.01)

    card = {
        "type": "product_card",
        "data": {
            "product_id": "p_demo_001",
            "title": "Demo Phone Pro",
            "price": 2899,
            "image_url": "",
            "reason": "符合预算，主摄和续航表现更适合日常拍照需求。",
        },
    }
    yield {"event": "message", "data": json.dumps(card, ensure_ascii=False)}
    yield {"event": "done", "data": "{}"}


@router.post("/stream")
async def stream_chat(request: ChatStreamRequest) -> EventSourceResponse:
    return EventSourceResponse(demo_chat_events(request))
