from liveinsight_core.agents.state import AgentWorkflowState
from liveinsight_core.agents.tools import rank_highlight_segments, summarize_sales_moments


class LiveInsightWorkflow:
    """Small deterministic scaffold for the future LangGraph workflow."""

    def run(self, state: AgentWorkflowState) -> AgentWorkflowState:
        state.trace.append("orchestrator: received task")
        state.trace.append("video_agent: loaded structured segments")
        state.trace.append("data_agent: analyzed sales moments")
        sales_summary = summarize_sales_moments(state.segments)

        state.trace.append("highlight_agent: ranked highlight clips")
        highlights = rank_highlight_segments(state.segments)

        state.report = (
            f"{sales_summary}\n"
            f"Found {len(highlights)} candidate highlight clips. "
            "The production workflow will enrich this with RAG evidence and model-generated recommendations."
        )
        state.scripts = [
            "Hook: This livestream moment explains why users started asking questions and converting.",
            "Storyboard: product close-up -> user question -> discount proof -> action reminder.",
        ]
        state.trace.append("content_agent: drafted report and script placeholders")
        return state
