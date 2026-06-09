from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter()


class KnowledgeIngestRequest(BaseModel):
    """商品知识入库请求。

    MVP 阶段先支持直接传入文本内容；后续可以扩展为 PDF、Word、图片、
    营销活动文档等非结构化资料上传。
    """

    product_id: str
    title: str
    content: str


@router.post("/ingest")
async def ingest_knowledge(request: KnowledgeIngestRequest) -> dict[str, object]:
    """商品知识入库接口占位实现。

    后续真实流程会包括：文档解析、文本切分、Embedding、向量入库、
    关键词索引和结构化字段抽取。
    """

    return {
        "status": "accepted",
        "product_id": request.product_id,
        "title": request.title,
        "chunks_created": 0,
    }
