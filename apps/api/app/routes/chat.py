import asyncio
import json
from collections.abc import AsyncIterator
from pathlib import Path

from fastapi import APIRouter
from pydantic import BaseModel
from sse_starlette.sse import EventSourceResponse

router = APIRouter()


class ChatStreamRequest(BaseModel):
    """客户端发起导购对话时的请求体。"""

    session_id: str
    message: str
    image_url: str | None = None


def load_sample_product() -> dict[str, object]:
    """读取本地 sample 商品数据。

    这一步模拟后续的商品库查询；等 PostgreSQL 接好后可以替换成真实查询。
    """

    project_root = Path(__file__).resolve().parents[4]
    products_file = project_root / "data" / "samples" / "products.json"
    products = json.loads(products_file.read_text(encoding="utf-8"))
    return products[0]


def build_demo_answer(user_message: str, product: dict[str, object]) -> str:
    """根据用户问题和 sample 商品生成一段导购回复。

    当前版本是规则拼接，用来跑通前后端交互闭环；
    后续会替换成 RAG 检索结果 + 大模型生成。
    """

    title = product["title"]
    price = product["price"]
    attributes = product.get("attributes", {})
    camera = attributes.get("camera", "拍照能力较好") if isinstance(attributes, dict) else "拍照能力较好"
    battery = attributes.get("battery", "续航表现较好") if isinstance(attributes, dict) else "续航表现较好"

    return (
        f"我根据你的问题「{user_message}」先做了一次本地商品样例匹配。"
        f"当前更推荐 {title}，价格约 {price} 元，符合 3000 以内的预算。"
        f"它的核心优势是 {camera} 和 {battery}，比较适合重视拍照、续航和性价比的用户。"
        "需要注意的是，它不是专业游戏手机，长焦能力也不如旗舰机型。"
        "如果你更看重游戏性能或轻薄手感，我可以继续帮你换一组筛选条件。"
    )


async def demo_chat_events(request: ChatStreamRequest) -> AsyncIterator[dict[str, str]]:
    """演示版 SSE 流式事件生成器。

    当前用本地 sample 商品模拟检索结果，再流式返回导购回复和商品卡片。
    后续会替换为：意图识别 -> RAG 检索 -> LLM 流式生成 -> 商品卡片事件。
    """

    product = load_sample_product()
    text = build_demo_answer(request.message, product)
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
            "product_id": product["id"],
            "title": product["title"],
            "price": product["price"],
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
