from liveinsight_core.domain import VideoSegment


def align_comments_to_segments(
    segments: list[VideoSegment], timed_comments: list[tuple[float, str]]
) -> list[VideoSegment]:
    for timestamp, comment in timed_comments:
        for segment in segments:
            if segment.start_time <= timestamp < segment.end_time:
                segment.comments.append(comment)
                break
    return segments
