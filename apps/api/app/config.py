from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_env: str = "local"
    app_name: str = "shopping-guide-agent"

    # Qdrant Cloud
    qdrant_url: str = "http://localhost:6333"
    qdrant_api_key: str | None = None
    qdrant_collection: str = "product_knowledge"

    # LLM (DeepSeek or any OpenAI-compatible)
    openai_api_key: str | None = None
    openai_base_url: str | None = None
    llm_model: str = "deepseek-chat"

    # Embedding (SiliconFlow bge-m3)
    siliconflow_api_key: str | None = None
    embedding_base_url: str = "https://api.siliconflow.cn/v1"
    embedding_model: str = "BAAI/bge-m3"

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


settings = Settings()
