from liveinsight_core.domain import VideoSegment


class MultimodalPipeline:
    """Video-to-timeline scaffold.

    Production implementation will call FFmpeg, ASR, OCR, keyframe extraction, VLM captioning,
    comment alignment, and metric alignment.
    """

    def parse_video(self, video_path: str, segment_seconds: int = 10) -> list[VideoSegment]:
        return [
            VideoSegment(
                segment_id="seg_0001",
                start_time=0,
                end_time=segment_seconds,
                asr_text="Demo ASR transcript will appear here.",
                ocr_text=["Demo OCR text"],
                visual_summary=f"Placeholder visual summary for {video_path}",
                comments=["Is there a coupon?", "Can sensitive skin use it?"],
                sales_delta=12,
                click_delta=230,
                emotion_score=0.65,
                conversion_score=0.7,
                highlight_score=0.74,
            )
        ]
