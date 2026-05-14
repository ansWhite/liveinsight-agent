from app.schemas.analysis import AnalysisRequest, AnalysisStatus, ChatRequest, ChatResponse
from app.schemas.report import HighlightClip, InsightReport, ScriptDraft


class AnalysisService:
    def __init__(self) -> None:
        self._tasks: dict[str, AnalysisStatus] = {}

    def start_analysis(self, payload: AnalysisRequest) -> AnalysisStatus:
        status = AnalysisStatus(
            project_id=payload.project_id,
            status="completed",
            progress=100,
            current_step="demo workflow completed",
        )
        self._tasks[status.task_id] = status
        return status

    def get_status(self, task_id: str) -> AnalysisStatus:
        return self._tasks.get(
            task_id,
            AnalysisStatus(project_id="unknown", status="failed", progress=0, current_step="task not found"),
        )

    def get_report(self, project_id: str) -> InsightReport:
        return InsightReport(
            project_id=project_id,
            summary="Demo report placeholder: the full workflow will combine ASR, OCR, RAG, metrics, and agent reasoning.",
            strengths=["Clear product discount messaging", "Potential high-engagement Q&A segments"],
            risks=["Missing real parsed video data", "Model evaluation has not been run yet"],
            user_questions=["Is this product suitable for sensitive skin?", "How do I claim the coupon?"],
            next_session_actions=["Strengthen the first 30-second hook", "Prepare a comparison slide against the top competitor"],
        )

    def get_highlights(self, project_id: str) -> list[HighlightClip]:
        return [
            HighlightClip(
                start_time=112.0,
                end_time=156.0,
                score=88.5,
                reason="The segment combines discount OCR, product demonstration, and dense user questions.",
                suggested_title="The 40 seconds that drove the livestream conversion spike",
            )
        ]

    def get_scripts(self, project_id: str) -> list[ScriptDraft]:
        return [
            ScriptDraft(
                title="Sensitive skin buyers should check these three details first",
                hook="Do not buy another moisturizer until you verify these three points.",
                voiceover=[
                    "First, check whether the product addresses your main skin concern.",
                    "Second, compare the promotion with the normal shelf price.",
                    "Third, look at real user questions from the livestream.",
                ],
                storyboard=[
                    "Open with product close-up and price overlay.",
                    "Cut to host demonstration and user question screenshot.",
                    "End with a concise offer recap.",
                ],
                cover_copy="Sensitive skin moisturizer checklist",
            )
        ]

    def chat(self, payload: ChatRequest) -> ChatResponse:
        return ChatResponse(
            answer=(
                "This is a scaffolded response. The production path will route the question through "
                "Product RAG Agent, Data Analysis Agent, and Report Agent."
            ),
            sources=["demo://agent-service"],
        )


analysis_service = AnalysisService()
