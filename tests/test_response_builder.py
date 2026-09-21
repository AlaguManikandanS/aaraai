from rag.pipeline.response_builder import build_response
from rag.retrieval.models import RetrievedChunk


def test_build_response_contains_answer_and_sources():
    chunks = [
        RetrievedChunk(
            score=0.91,
            document_id="agam-paper-001",
            page_number=5,
            chunk_index=10,
            text="Agam uses a fine-tuned BERT model.",
        ),
        RetrievedChunk(
            score=0.82,
            document_id="agam-paper-001",
            page_number=8,
            chunk_index=20,
            text="Agam performs cognitive distortion detection.",
        ),
    ]

    result = build_response(
        answer="Agam uses a fine-tuned BERT model.",
        retrieved_chunks=chunks,
    )

    assert result["answer"] == "Agam uses a fine-tuned BERT model."

    assert result["sources"][0]["page_number"] == 5
    assert result["sources"][0]["chunk_index"] == 10
    assert result["sources"][0]["score"] == 0.91

    assert result["sources"][1]["page_number"] == 8