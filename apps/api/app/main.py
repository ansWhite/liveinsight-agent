from fastapi import FastAPI

from app.routes.chat import router as chat_router
from app.routes.health import router as health_router
from app.routes.knowledge import router as knowledge_router
from app.routes.products import router as products_router

app = FastAPI(
    title="Multimodal RAG Shopping Guide Agent API",
    version="0.1.0",
)

app.include_router(health_router, prefix="/api/v1", tags=["health"])
app.include_router(chat_router, prefix="/api/v1/chat", tags=["chat"])
app.include_router(knowledge_router, prefix="/api/v1/knowledge", tags=["knowledge"])
app.include_router(products_router, prefix="/api/v1/products", tags=["products"])
