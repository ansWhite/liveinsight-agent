from pydantic import BaseModel, Field


class VideoSegment(BaseModel):
    segment_id: str
    start_time: float
    end_time: float
    asr_text: str = ""
    ocr_text: list[str] = Field(default_factory=list)
    visual_summary: str = ""
    comments: list[str] = Field(default_factory=list)
    sales_delta: float = 0.0
    click_delta: float = 0.0
    emotion_score: float = 0.0
    conversion_score: float = 0.0
    highlight_score: float = 0.0


class AgentEvidence(BaseModel):
    source_type: str
    source_id: str
    quote: str
    confidence: float = 0.0


class AgentFinding(BaseModel):
    title: str
    detail: str
    evidence: list[AgentEvidence] = Field(default_factory=list)
    confidence: float = 0.0
