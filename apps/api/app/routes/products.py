from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter()


class ProductSearchRequest(BaseModel):
    """商品搜索请求。

    query 是用户自然语言需求，filters 用来承载价格、品类、品牌等结构化约束。
    """

    query: str
    filters: dict[str, object] | None = None


@router.post("/search")
async def search_products(request: ProductSearchRequest) -> dict[str, object]:
    """商品搜索接口占位实现。

    后续会连接 PostgreSQL 商品库，并结合结构化过滤、排序和推荐理由生成。
    """

    return {
        "query": request.query,
        "filters": request.filters or {},
        "items": [
            {
                "product_id": "p_demo_001",
                "title": "Demo Phone Pro",
                "price": 2899,
                "reason": "示例商品，用于前后端联调。",
            }
        ],
    }
