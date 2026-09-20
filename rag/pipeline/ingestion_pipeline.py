import uuid

from qdrant_client.models import PointStruct

from rag.ingestion.pdf_loader import load_pdf
from rag.processing.chunker import chunk_documents
from rag.processing.embedder import EmbeddingModel
from rag.retrieval.vector_store import VectorStore


class IngestionPipeline:
    def __init__(self, collection_name="aaraai_chunks"):
        self.embedder = EmbeddingModel()

        self.vector_store = VectorStore(
            collection_name=collection_name,
            vector_size=self.embedder.dimension,
        )

    def ingest(self, pdf_path, document_id):
        pages = load_pdf(pdf_path)

        chunks = chunk_documents(pages)

        texts = [chunk["text"] for chunk in chunks]

        embeddings = self.embedder.encode(texts)

        points = []

        for chunk, embedding in zip(chunks, embeddings):
            point_id = str(uuid.uuid4())

            payload = {
                "document_id": document_id,
                "page_number": chunk["page_number"],
                "chunk_index": chunk["chunk_index"],
                "text": chunk["text"],
            }

            point = PointStruct(
                id=point_id,
                vector=embedding.tolist(),
                payload=payload,
            )

            points.append(point)

        self.vector_store.add(points)

        return {
            "document_id": document_id,
            "pages": len(pages),
            "chunks": len(chunks),
        }