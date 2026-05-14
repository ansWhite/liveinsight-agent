from liveinsight_core.domain import VideoSegment
from liveinsight_core.training.datasets import SegmentClassificationExample


def build_segment_classification_examples(
    segments: list[VideoSegment],
) -> list[SegmentClassificationExample]:
    examples: list[SegmentClassificationExample] = []
    for segment in segments:
        text = "\n".join(
            [
                f"ASR: {segment.asr_text}",
                f"OCR: {'; '.join(segment.ocr_text)}",
                f"COMMENTS: {'; '.join(segment.comments)}",
            ]
        )
        label = "high_conversion" if segment.sales_delta > 50 else "normal"
        examples.append(SegmentClassificationExample(text=text, label=label, sales_delta=segment.sales_delta))
    return examples
