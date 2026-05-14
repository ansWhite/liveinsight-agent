from pydantic import BaseModel


class RerankerExample(BaseModel):
    query: str
    positive: str
    negative: str


class SegmentClassificationExample(BaseModel):
    text: str
    label: str
    sales_delta: float = 0.0


class ScriptPreferenceExample(BaseModel):
    prompt: str
    chosen: str
    rejected: str


class AgentTrajectoryExample(BaseModel):
    user_task: str
    tool_calls: list[str]
    final_answer: str
