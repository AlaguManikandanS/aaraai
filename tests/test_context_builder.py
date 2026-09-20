from rag.pipeline.context_builder import build_context
from rag.retrieval.models import RetrievedChunk


def test_build_context_formats_retrieved_chunks():
    chunks = [
        RetrievedChunk(
            score=0.90,
            document_id="agam-paper-001",
            page_number=5,
            chunk_index=10,
            text="Agam uses a fine-tuned BERT model.",
        ),
        RetrievedChunk(
            score=0.80,
            document_id="agam-paper-001",
            page_number=8,
            chunk_index=20,
            text="The system analyzes user journaling data.",
        ),
    ]

    context = build_context(chunks)

    assert "[Page 5]" in context
    assert "Agam uses a fine-tuned BERT model." in context

    assert "[Page 8]" in context
    assert "The system analyzes user journaling data." in context