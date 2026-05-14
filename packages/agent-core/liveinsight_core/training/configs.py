from pydantic import BaseModel


class LoRAConfig(BaseModel):
    base_model: str = "Qwen/Qwen2.5-7B-Instruct"
    r: int = 8
    alpha: int = 16
    dropout: float = 0.05
    target_modules: list[str] = ["q_proj", "v_proj"]


class DPOConfig(BaseModel):
    base_model: str = "Qwen/Qwen2.5-7B-Instruct"
    beta: float = 0.1
    max_prompt_length: int = 1024
    max_length: int = 2048


class RerankerTrainConfig(BaseModel):
    base_model: str = "BAAI/bge-reranker-base"
    learning_rate: float = 2e-5
    epochs: int = 2
    batch_size: int = 16
