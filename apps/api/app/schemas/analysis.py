from datetime import datetime
from typing import Literal
from uuid import uuid4

from pydantic import BaseModel, Field


class AnalysisRequest(BaseModel):
    project_id: str
    include_competitor_analysis: bool = True
    generate_scripts: bool = True


class AnalysisStatus(BaseModel):
    task_id: str = Field(default_factory=lambda: str(uuid4()))
    project_id: str
    status: Literal["queued", "running", "completed", "failed"] = "queued"
    progress: int = 0
    current_step: str = "queued"
    created_at: datetime = Field(default_factory=datetime.utcnow)


class ChatRequest(BaseModel):
    project_id: str
    message: str


class ChatResponse(BaseModel):
    answer: str
    sources: list[str] = Field(default_factory=list)
