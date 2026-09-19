from rag.processing.chunker import chunk_documents


def test_chunk_documents_splits_text():
    pages = [
        {
            "page_number": 1,
            "text": "A" * 2500,
        }
    ]

    chunks = chunk_documents(
        pages,
        chunk_size=1000,
        overlap=100,
    )

    assert len(chunks) == 3
    assert chunks[0]["chunk_index"] == 0
    assert chunks[1]["chunk_index"] == 1
    assert chunks[2]["chunk_index"] == 2
    assert chunks[0]["page_number"] == 1


def test_chunk_documents_preserves_paragraphs():
    pages = [
        {
            "page_number": 1,
            "text": (
                "This is the introduction paragraph.\n\n"
                "This paragraph explains the methodology.\n\n"
                "This paragraph discusses the results."
            ),
        }
    ]

    chunks = chunk_documents(
        pages,
        chunk_size=100,
        overlap=20,
    )

    assert len(chunks) >= 2
    assert chunks[0]["page_number"] == 1
    assert chunks[0]["chunk_index"] == 0