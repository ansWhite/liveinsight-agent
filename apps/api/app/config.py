from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_env: str = "local"
    app_name: str = "shopping-guide-agent"
    qdrant_url: str = "http://localhost:6333"
    qdrant_collection: str = "product_knowledge"
    openai_api_key: str | None = None
    openai_base_url: str | None = None
    llm_model: str | None = None
    embedding_model: str | None = None

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


settings = Settings()
