import asyncio
import json
from collections.abc import AsyncIterator

from fastapi import APIRouter
from pydantic import BaseModel
from sse_starlette.sse import EventSourceResponse

router = APIRouter()


class ChatStreamRequest(BaseModel):
    """客户端发起导购对话时的请求体。"""

    session_id: str
    message: str
    image_url: str | None = None


async def demo_chat_events(request: ChatStreamRequest) -> AsyncIterator[dict[str, str]]:
    """演示版 SSE 流式事件生成器。

    当前还没有真正接入 RAG 和大模型，所以这里用固定文本模拟逐字输出。
    后续会替换为：意图识别 -> 检索 -> LLM 流式生成 -> 商品卡片事件。
    """

    text = (
        "我会先结合你的预算、使用场景和商品知识库做检索，"
        "再给出推荐理由和可对比的商品卡片。"
    )
    for char in text:
        # text_delta 表示一小段模型回复，客户端收到后追加到聊天气泡里。
        yield {
            "event": "message",
            "data": json.dumps({"type": "text_delta", "content": char}, ensure_ascii=False),
        }
        await asyncio.sleep(0.01)

    # product_card 是结构化商品卡片事件，客户端按 schema 渲染商品推荐。
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
    """导购对话流式接口。

    使用 SSE 返回模型文本和商品卡片事件，适合实现类似豆包的逐字输出体验。
    """

    return EventSourceResponse(demo_chat_events(request))
