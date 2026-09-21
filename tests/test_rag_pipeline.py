import numpy as np

from rag.pipeline.rag_pipeline import RAGPipeline
from rag.retrieval.models import RetrievedChunk


def test_rag_pipeline_returns_answer():
    pipeline = RAGPipeline.__new__(RAGPipeline)

    class FakeEmbedder:
        def encode(self, texts):
            return np.array([[1.0, 0.0, 0.0]])

    class FakeVectorStore:
        def search(self, query_vector, document_id, limit):
            return [
                RetrievedChunk(
                    score=0.91,
                    document_id=document_id,
                    page_number=5,
                    chunk_index=10,
                    text="Agam uses a fine-tuned BERT model.",
                )
            ]

    class FakeLLM:
        def generate(self, prompt):
            assert "Agam uses a fine-tuned BERT model." in prompt
            assert "What model does Agam use?" in prompt

            # The LLM should generate only the answer.
            # Aaraai adds verified page citations separately.
            return "Agam uses a fine-tuned BERT model."

    pipeline.embedder = FakeEmbedder()
    pipeline.vector_store = FakeVectorStore()
    pipeline.llm = FakeLLM()

    result = pipeline.ask(
        question="What model does Agam use?",
        document_id="agam-paper-001",
    )

    assert result["answer"] == (
        "Agam uses a fine-tuned BERT model. [Page 5]"
    )

    assert result["sources"][0]["page_number"] == 5
    assert result["sources"][0]["chunk_index"] == 10


def test_rag_pipeline_handles_no_retrieved_chunks():
    pipeline = RAGPipeline.__new__(RAGPipeline)

    class FakeEmbedder:
        def encode(self, texts):
            return np.array([[1.0, 0.0, 0.0]])

    class FakeVectorStore:
        def search(self, query_vector, document_id, limit):
            return []

    class FakeLLM:
        def generate(self, prompt):
            raise AssertionError("LLM should not be called")

    pipeline.embedder = FakeEmbedder()
    pipeline.vector_store = FakeVectorStore()
    pipeline.llm = FakeLLM()

    result = pipeline.ask(
        question="What model does Agam use?",
        document_id="agam-paper-001",
    )

    assert result["answer"] == (
        "I couldn't find relevant information in the paper."
    )

    assert result["sources"] == []