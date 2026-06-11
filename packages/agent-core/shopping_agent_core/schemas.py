from pydantic import BaseModel


class ProductCard(BaseModel):
    """商品卡片结构。

    后端以这个结构返回推荐商品，客户端据此渲染图片、价格和推荐理由。
    """

    product_id: str
    title: str
    price: float | None = None
    image_url: str | None = None
    reason: str


class RetrievalChunk(BaseModel):
    """RAG 检索返回的知识片段。

    Agent 生成答案时应该基于这些片段，而不是直接凭模型记忆编造事实。
    """

    chunk_id: str
    product_id: str | None = None
    text: str
    score: float
    source: str | None = None


class ChunkRecord(BaseModel):
    """Internal record produced by the chunker before embedding and storage."""

    chunk_id: str
    product_id: str
    source: str
    chunk_text: str
    chunk_index: int
