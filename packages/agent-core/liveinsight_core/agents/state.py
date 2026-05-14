from pydantic import BaseModel, Field

from liveinsight_core.domain import AgentFinding, VideoSegment


class AgentWorkflowState(BaseModel):
    project_id: str
    user_task: str
    segments: list[VideoSegment] = Field(default_factory=list)
    retrieved_context: list[str] = Field(default_factory=list)
    findings: list[AgentFinding] = Field(default_factory=list)
    report: str = ""
    scripts: list[str] = Field(default_factory=list)
    trace: list[str] = Field(default_factory=list)
