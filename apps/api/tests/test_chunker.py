from shopping_agent_core.chunker import split


def test_split_creates_one_chunk_per_paragraph():
    content = "Para one.\n\nPara two.\n\nPara three."
    chunks = split(content, source="Test Doc", product_id="p001")
    assert len(chunks) == 3


def test_split_chunk_metadata():
    chunks = split("Only paragraph.", source="My Doc", product_id="p_abc")
    assert chunks[0].product_id == "p_abc"
    assert chunks[0].source == "My Doc"
    assert chunks[0].chunk_index == 0


def test_split_long_paragraph_is_broken_down():
    # Single paragraph longer than 500 chars must be split
    long_para = ("This is a long sentence. " * 25).strip()  # ~625 chars
    chunks = split(long_para, source="Test", product_id="p001")
    assert len(chunks) > 1
    for chunk in chunks:
        assert len(chunk.chunk_text) <= 600  # allow small overflow at sentence boundary


def test_split_overlap_includes_last_sentence_of_previous():
    content = "First sentence. Second sentence.\n\nThird sentence."
    chunks = split(content, source="Test", product_id="p001")
    # Second chunk should contain the last sentence of the first paragraph
    assert "Second sentence." in chunks[1].chunk_text
    assert "Third sentence." in chunks[1].chunk_text


def test_split_chunk_ids_are_unique():
    content = "Para one.\n\nPara two.\n\nPara three."
    chunks = split(content, source="Test", product_id="p001")
    ids = [c.chunk_id for c in chunks]
    assert len(ids) == len(set(ids))


def test_split_empty_content_returns_empty():
    assert split("", source="Test", product_id="p001") == []


def test_split_ignores_blank_only_paragraphs():
    content = "Para one.\n\n   \n\nPara two."
    chunks = split(content, source="Test", product_id="p001")
    assert len(chunks) == 2
