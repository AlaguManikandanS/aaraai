from qdrant_client.models import PointStruct

from rag.retrieval.vector_store import VectorStore


def test_vector_store_adds_and_searches_points():
    store = VectorStore()

    points = [
        PointStruct(
            id=1,
            vector=[1.0] + [0.0] * 383,
            payload={
                "text": "Medical image classification",
                "page_number": 2,
            },
        ),
        PointStruct(
            id=2,
            vector=[0.0, 1.0] + [0.0] * 382,
            payload={
                "text": "Hospital dataset information",
                "page_number": 4,
            },
        ),
    ]

    store.add(points)

    results = store.search(
        query_vector=[1.0] + [0.0] * 383,
        limit=1,
    )

    assert len(results) == 1
    assert results[0].id == 1
    assert results[0].payload["page_number"] == 2