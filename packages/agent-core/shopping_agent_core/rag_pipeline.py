import json
from collections.abc import AsyncIterator
from pathlib import Path

from shopping_agent_core.chunker import split as chunk_split
from shopping_agent_core.llm_client import LLMClient
from shopping_agent_core.prompts import SHOPPING_GUIDE_SYSTEM_PROMPT
from shopping_agent_core.retriever import Retriever
from shopping_agent_core.schemas import RetrievalChunk


class RAGPipeline:
    def __init__(
        self,
        retriever: Retriever,
        llm_client: LLMClient,
        products_file: Path | None = None,
    ) -> None:
        self._retriever = retriever
        self._llm_client = llm_client
        self._products_file = products_file

    async def ingest(self, product_id: str, title: str, content: str) -> int:
        chunks = chunk_split(content, source=title, product_id=product_id)
        vectors = await self._retriever.embedder.embed([c.chunk_text for c in chunks])
        return await self._retriever.vectorstore.upsert(chunks, vectors)

    def _build_messages(self, chunks: list[RetrievalChunk], user_message: str) -> list[dict]:
        if chunks:
            context_lines = [
                f"[{i + 1}] {c.source or 'unknown'}\n{c.text}"
                for i, c in enumerate(chunks)
            ]
            system = SHOPPING_GUIDE_SYSTEM_PROMPT + "\n\nProduct knowledge:\n" + "\n\n".join(context_lines)
        else:
            system = (
                SHOPPING_GUIDE_SYSTEM_PROMPT
                + "\n\nNo product knowledge was retrieved. "
                "Tell the user honestly that you don't have relevant product information."
            )
        return [
            {"role": "system", "content": system},
            {"role": "user", "content": user_message},
        ]

    def _load_product_cards(self, product_ids: list[str]) -> list[dict]:
        if not self._products_file or not self._products_file.exists():
            return []
        products: list[dict] = json.loads(self._products_file.read_text(encoding="utf-8"))
        seen: set[str] = set()
        cards: list[dict] = []
        for pid in product_ids:
            if pid in seen:
                continue
            seen.add(pid)
            for p in products:
                if p["id"] == pid:
                    cards.append(
                        {
                            "product_id": p["id"],
                            "title": p["title"],
                            "price": p.get("price"),
                            "image_url": p.get("main_image_url", ""),
                            "reason": "Based on retrieved product knowledge.",
                        }
                    )
        return cards

    async def stream_answer(self, user_message: str) -> AsyncIterator[dict]:
        chunks = await self._retriever.retrieve(user_message, top_k=5)
        messages = self._build_messages(chunks, user_message)

        async for token in self._llm_client.stream_chat(messages):
            yield {"type": "text_delta", "content": token}

        product_ids = [c.product_id for c in chunks if c.product_id]
        for card in self._load_product_cards(product_ids):
            yield {"type": "product_card", "data": card}
