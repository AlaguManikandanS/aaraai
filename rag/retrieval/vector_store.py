import os

from rag.retrieval.models import RetrievedChunk

from dotenv import load_dotenv
from qdrant_client import QdrantClient
from qdrant_client.models import (
    Distance,
    FieldCondition,
    Filter,
    MatchValue,
    PointStruct,
    VectorParams,
)

load_dotenv()


class VectorStore:
    def __init__(self, collection_name="aaraai_chunks", vector_size=384):
        qdrant_url = os.getenv(
            "QDRANT_URL",
            "http://localhost:6333",
        )

        self.client = QdrantClient(url=qdrant_url)
        self.collection_name = collection_name

        if not self.client.collection_exists(self.collection_name):
            self.client.create_collection(
                collection_name=self.collection_name,
                vectors_config=VectorParams(
                    size=vector_size,
                    distance=Distance.COSINE,
                ),
            )

    def add(self, points):
        self.client.upsert(
            collection_name=self.collection_name,
            points=points,
        )

    def search(self, query_vector, document_id=None, limit=3):
        query_filter = None

        if document_id is not None:
            query_filter = Filter(
                must=[
                    FieldCondition(
                        key="document_id",
                        match=MatchValue(value=document_id),
                    )
                ]
            )

        points = self.client.query_points(
            collection_name=self.collection_name,
            query=query_vector,
            query_filter=query_filter,
            limit=limit,
        ).points

        results = []

        for point in points:
            results.append(
                RetrievedChunk(
                    score=point.score,
                    document_id=point.payload["document_id"],
                    page_number=point.payload["page_number"],
                    chunk_index=point.payload["chunk_index"],
                    text=point.payload["text"],
                )
            )

        return results