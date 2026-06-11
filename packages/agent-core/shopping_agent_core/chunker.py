import re
import uuid

from shopping_agent_core.schemas import ChunkRecord

_MAX_CHARS = 500


def _chunk_id(product_id: str, index: int) -> str:
    return str(uuid.uuid5(uuid.NAMESPACE_OID, f"{product_id}:{index}"))


def _split_long(text: str, max_chars: int) -> list[str]:
    sentences = re.split(r"(?<=[.。!?！？])\s+", text)
    parts: list[str] = []
    current = ""
    for sentence in sentences:
        if current and len(current) + 1 + len(sentence) > max_chars:
            parts.append(current)
            current = sentence
        else:
            current = (current + " " + sentence).strip() if current else sentence
    if current:
        parts.append(current)
    return parts or [text]


def split(
    content: str,
    source: str,
    product_id: str,
    max_chars: int = _MAX_CHARS,
) -> list[ChunkRecord]:
    if not content.strip():
        return []

    paragraphs = [p.strip() for p in re.split(r"\n\n+", content) if p.strip()]

    raw: list[str] = []
    for para in paragraphs:
        if len(para) <= max_chars:
            raw.append(para)
        else:
            raw.extend(_split_long(para, max_chars))

    # Overlap: prepend last sentence of previous raw chunk
    with_overlap: list[str] = []
    for i, chunk in enumerate(raw):
        if i == 0:
            with_overlap.append(chunk)
        else:
            prev_sentences = re.split(r"(?<=[.。!?！？])\s+", raw[i - 1])
            overlap = prev_sentences[-1] if prev_sentences else ""
            with_overlap.append((overlap + " " + chunk).strip() if overlap else chunk)

    return [
        ChunkRecord(
            chunk_id=_chunk_id(product_id, i),
            product_id=product_id,
            source=source,
            chunk_text=text,
            chunk_index=i,
        )
        for i, text in enumerate(with_overlap)
    ]
