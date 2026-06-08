from pydantic import BaseModel


class ProductCard(BaseModel):
    product_id: str
    title: str
    price: float | None = None
    image_url: str | None = None
    reason: str


class RetrievalChunk(BaseModel):
    chunk_id: str
    product_id: str | None = None
    text: str
    score: float
    source: str | None = None
