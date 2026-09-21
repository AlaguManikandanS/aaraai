from rag.generation.llm_client import LLMClient
from rag.pipeline.context_builder import build_context
from rag.pipeline.prompt_builder import build_prompt
from rag.pipeline.response_builder import build_response
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