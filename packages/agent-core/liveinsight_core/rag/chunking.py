from dataclasses import dataclass


@dataclass(frozen=True)
class Chunk:
    chunk_id: str
    text: str
    metadata: dict[str, str]


def chunk_text(document_id: str, text: str, chunk_size: int = 800, overlap: int = 120) -> list[Chunk]:
    chunks: list[Chunk] = []
    start = 0
    index = 0
    while start < len(text):
        end = min(start + chunk_size, len(text))
        chunks.append(
            Chunk(
                chunk_id=f"{document_id}:{index}",
                text=text[start:end],
                metadata={"document_id": document_id, "chunk_index": str(index)},
            )
        )
        if end == len(text):
            break
        start = max(0, end - overlap)
        index += 1
    return chunks
