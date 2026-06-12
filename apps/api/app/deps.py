from functools import cache
from pathlib import Path

from shopping_agent_core.embedder import Embedder
from shopping_agent_core.llm_client import LLMClient
from shopping_agent_core.rag_pipeline import RAGPipeline
from shopping_agent_core.retriever import Retriever
from shopping_agent_core.vectorstore import VectorStore

from app.config import settings

_PRODUCTS_FILE = Path(__file__).resolve().parents[3] / "data" / "samples" / "products.json"


@cache
def get_rag_pipeline() -> RAGPipeline:
    embedder = Embedder(
        api_key=settings.siliconflow_api_key or "",
        base_url=settings.embedding_base_url,
        model=settings.embedding_model,
    )
    vectorstore = VectorStore(
        url=settings.qdrant_url,
        api_key=settings.qdrant_api_key,
        collection=settings.qdrant_collection,
    )
    retriever = Retriever(embedder=embedder, vectorstore=vectorstore)
    llm_client = LLMClient(
        api_key=settings.openai_api_key or "",
        base_url=settings.openai_base_url or "https://api.deepseek.com/v1",
        model=settings.llm_model,
    )
    return RAGPipeline(
        retriever=retriever,
        llm_client=llm_client,
        products_file=_PRODUCTS_FILE,
    )
