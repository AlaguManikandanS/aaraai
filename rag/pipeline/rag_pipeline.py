from rag.generation.llm_client import LLMClient
from rag.pipeline.context_builder import build_context
from rag.pipeline.prompt_builder import build_prompt
from rag.pipeline.response_builder import build_response
from rag.pipeline.summary_prompt_builder import build_summary_prompt
from rag.processing.embedder import EmbeddingModel
from rag.retrieval.vector_store import VectorStore


class RAGPipeline:
    def __init__(self, collection_name="aaraai_chunks"):
        self.embedder = EmbeddingModel()

        self.vector_store = VectorStore(
            collection_name=collection_name,
            vector_size=self.embedder.dimension,
        )

        self.llm = LLMClient()

    def ask(self, question, document_id, top_k=3):
        if not question.strip():
            raise ValueError("question cannot be empty")

        if not document_id.strip():
            raise ValueError("document_id cannot be empty")

        query_embedding = self.embedder.encode([question])[0]

        retrieved_chunks = self.vector_store.search(
            query_vector=query_embedding.tolist(),
            document_id=document_id,
            limit=top_k,
        )

        if not retrieved_chunks:
            return {
                "answer": "I couldn't find relevant information in the paper.",
                "sources": [],
            }

        context = build_context(retrieved_chunks)

        prompt = build_prompt(
            question=question,
            context=context,
        )

        answer = self.llm.generate(prompt)

        return build_response(
            answer=answer,
            retrieved_chunks=retrieved_chunks,
        )

    def summarize(self, document_id):
        if not document_id.strip():
            raise ValueError("document_id cannot be empty")

        document_chunks = self.vector_store.get_document_chunks(
            document_id
        )

        if not document_chunks:
            return {
                "overview": "I couldn't find any content in the paper.",
                "sources": [],
            }

        context = build_context(document_chunks)

        prompt = build_summary_prompt(context)

        overview = self.llm.generate(prompt)

        pages = sorted(
            {
                chunk.page_number
                for chunk in document_chunks
            }
        )

        return {
            "overview": overview.strip(),
            "sources": [
                {"page_number": page}
                for page in pages
            ],
        }