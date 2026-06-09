from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """统一读取环境变量配置。

    后续接入数据库、向量库和大模型时，尽量都从这里读取配置，
    避免把密钥、模型名、服务地址硬编码在业务代码里。
    """

    app_env: str = "local"
    app_name: str = "shopping-guide-agent"
    qdrant_url: str = "http://localhost:6333"
    qdrant_collection: str = "product_knowledge"
    openai_api_key: str | None = None
    openai_base_url: str | None = None
    llm_model: str | None = None
    embedding_model: str | None = None

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


# 全局配置对象，其他模块可以直接 import 使用。
settings = Settings()
