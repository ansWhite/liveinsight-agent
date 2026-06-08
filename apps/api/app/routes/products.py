from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter()


class ProductSearchRequest(BaseModel):
    query: str
    filters: dict[str, object] | None = None


@router.post("/search")
async def search_products(request: ProductSearchRequest) -> dict[str, object]:
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
