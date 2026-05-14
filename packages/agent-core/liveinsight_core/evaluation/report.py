from pydantic import BaseModel


class EvaluationReport(BaseModel):
    rag_recall_at_5: float = 0.0
    rag_ndcg_at_10: float = 0.0
    highlight_top_k_hit_rate: float = 0.0
    tool_call_success_rate: float = 0.0
    script_preference_win_rate: float = 0.0

    def to_markdown(self) -> str:
        return "\n".join(
            [
                "# Evaluation Report",
                f"- RAG Recall@5: {self.rag_recall_at_5:.3f}",
                f"- RAG NDCG@10: {self.rag_ndcg_at_10:.3f}",
                f"- Highlight Top-K hit rate: {self.highlight_top_k_hit_rate:.3f}",
                f"- Tool-call success rate: {self.tool_call_success_rate:.3f}",
                f"- Script preference win rate: {self.script_preference_win_rate:.3f}",
            ]
        )
