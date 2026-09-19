from qdrant_client import QdrantClient
from qdrant_client.models import Distance, PointStruct, VectorParams


class VectorStore:
    def __init__(self, collection_name="aaraai_chunks"):
        self.client = QdrantClient(":memory:")
        self.collection_name = collection_name

        self.client.create_collection(
            collection_name=self.collection_name,
            vectors_config=VectorParams(
                size=384,
                distance=Distance.COSINE,
            ),
        )

    def add(self, points):
        self.client.upsert(
            collection_name=self.collection_name,
            points=points,
        )

    def search(self, query_vector, limit=3):
        return self.client.query_points(
            collection_name=self.collection_name,
            query=query_vector,
            limit=limit,
        ).points