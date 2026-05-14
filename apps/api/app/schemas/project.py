from datetime import datetime
from uuid import uuid4

from pydantic import BaseModel, Field


class ProjectCreate(BaseModel):
    name: str = Field(..., examples=["May skincare livestream replay"])
    description: str | None = None


class ProjectRead(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid4()))
    name: str
    description: str | None = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
