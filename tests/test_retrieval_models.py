from rag.retrieval.models import RetrievedChunk


def test_retrieved_chunk_stores_metadata():
    chunk = RetrievedChunk(
        score=0.85,
        document_id="document-A",
        page_number=5,
        chunk_index=12,
        text="BERT is used for cognitive distortion detection.",
    )

    assert chunk.score == 0.85
    assert chunk.document_id == "document-A"
    assert chunk.page_number == 5
    assert chunk.chunk_index == 12
    assert chunk.text == "BERT is used for cognitive distortion detection."