from liveinsight_core.domain import VideoSegment


def rank_highlight_segments(segments: list[VideoSegment], limit: int = 5) -> list[VideoSegment]:
    return sorted(segments, key=lambda item: item.highlight_score, reverse=True)[:limit]


def summarize_sales_moments(segments: list[VideoSegment]) -> str:
    if not segments:
        return "No sales timeline data is available."
    best = max(segments, key=lambda item: item.sales_delta)
    return (
        f"Peak sales movement appears around {best.start_time:.0f}s-{best.end_time:.0f}s "
        f"with sales delta {best.sales_delta:.1f}."
    )
