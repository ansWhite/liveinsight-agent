from pydantic import BaseModel, Field


class HighlightClip(BaseModel):
    start_time: float
    end_time: float
    score: float
    reason: str
    suggested_title: str


class ScriptDraft(BaseModel):
    title: str
    hook: str
    platform: str = "douyin"
    voiceover: list[str] = Field(default_factory=list)
    storyboard: list[str] = Field(default_factory=list)
    cover_copy: str


class InsightReport(BaseModel):
    project_id: str
    summary: str
    strengths: list[str] = Field(default_factory=list)
    risks: list[str] = Field(default_factory=list)
    user_questions: list[str] = Field(default_factory=list)
    next_session_actions: list[str] = Field(default_factory=list)
