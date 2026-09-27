from unittest.mock import Mock

from rag.pipeline.rag_pipeline import RAGPipeline
from rag.retrieval.models import RetrievedChunk


def test_rag_pipeline_summarizes_document():
    pipeline = RAGPipeline.__new__(RAGPipeline)

    pipeline.vector_store = Mock()
    pipeline.llm = Mock()

    pipeline.vector_store.get_document_chunks.return_value = [
        RetrievedChunk(
            score=0.0,
            document_id="document-A",
            page_number=3,
            chunk_index=2,
            text="Results of the research.",
        ),
        RetrievedChunk(
            score=0.0,
            document_id="document-A",
            page_number=1,
            chunk_index=0,
            text="Introduction to the research.",
        ),
        RetrievedChunk(
            score=0.0,
            document_id="document-A",
            page_number=2,
            chunk_index=1,
            text="Methodology of the research.",
        ),
    ]

    pipeline.llm.generate.return_value = (
        "OVERVIEW:\nAn AI-based adaptive learning system."
    )

    result = pipeline.summarize("document-A")

    assert "overview" in result
    assert "AI-based adaptive learning system" in result["overview"]

    assert result["sources"] == [
        {"page_number": 1},
        {"page_number": 2},
        {"page_number": 3},
    ]

    pipeline.vector_store.get_document_chunks.assert_called_once_with(
        "document-A"
    )

    pipeline.llm.generate.assert_called_once()