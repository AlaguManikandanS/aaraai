from rag.pipeline.response_builder import build_response
from rag.retrieval.models import RetrievedChunk


def test_build_response_contains_verified_page_citations():
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
        RetrievedChunk(
            score=0.75,
            document_id="agam-paper-001",
            page_number=5,
            chunk_index=11,
            text="BERT is fine-tuned for the task.",
        ),
    ]

    result = build_response(
        answer="Agam uses a fine-tuned BERT model.",
        retrieved_chunks=chunks,
    )

    assert result["answer"] == (
        "Agam uses a fine-tuned BERT model. [Page 5] [Page 8]"
    )

    assert result["sources"][0]["page_number"] == 5
    assert result["sources"][1]["page_number"] == 8
    assert result["sources"][2]["page_number"] == 5


def test_build_response_handles_empty_answer():
    chunks = [
        RetrievedChunk(
            score=0.90,
            document_id="agam-paper-001",
            page_number=5,
            chunk_index=10,
            text="Agam uses BERT.",
        )
    ]

    result = build_response(
        answer="",
        retrieved_chunks=chunks,
    )

    assert result["answer"] == "[Page 5]"