from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routes.chat import router as chat_router
from app.routes.health import router as health_router
from app.routes.knowledge import router as knowledge_router
from app.routes.products import router as products_router

# FastAPI 应用入口。
# 这里负责创建后端服务实例，并挂载各个业务路由模块。
app = FastAPI(
    title="Multimodal RAG Shopping Guide Agent API",
    version="0.1.0",
)

# 本地开发阶段允许前端 Demo 跨域访问后端。
# 生产环境要把 allow_origins 收紧为正式域名。
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 所有接口统一放在 /api/v1 前缀下，便于后续版本升级。
app.include_router(health_router, prefix="/api/v1", tags=["health"])
app.include_router(chat_router, prefix="/api/v1/chat", tags=["chat"])
app.include_router(knowledge_router, prefix="/api/v1/knowledge", tags=["knowledge"])
app.include_router(products_router, prefix="/api/v1/products", tags=["products"])
