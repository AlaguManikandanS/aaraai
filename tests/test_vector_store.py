from qdrant_client.models import PointStruct

from rag.retrieval.vector_store import VectorStore


def test_vector_store_adds_and_searches_points():
    store = VectorStore()

    points = [
        PointStruct(
            id=1,
            vector=[1.0] + [0.0] * 383,
            payload={
                "document_id": "document-A",
                "page_number": 2,
                "chunk_index": 0,
                "text": "Medical image classification",
            },
        ),
        PointStruct(
            id=2,
            vector=[0.0, 1.0] + [0.0] * 382,
            payload={
                "document_id": "document-A",
                "page_number": 4,
                "chunk_index": 1,
                "text": "Hospital dataset information",
            },
        ),
    ]

    store.add(points)

    results = store.search(
        query_vector=[1.0] + [0.0] * 383,
        limit=1,
    )

    assert len(results) == 1
    assert results[0].document_id == "document-A"
    assert results[0].page_number == 2
    assert results[0].chunk_index == 0
    assert results[0].text == "Medical image classification"


def test_vector_store_filters_by_document_id():
    store = VectorStore(
        collection_name="aaraai_document_filter_test"
    )

    points = [
        PointStruct(
            id=101,
            vector=[1.0] + [0.0] * 383,
            payload={
                "document_id": "document-A",
                "text": "BERT is used for text classification.",
                "page_number": 1,
                "chunk_index": 0,
            },
        ),
        PointStruct(
            id=102,
            vector=[1.0] + [0.0] * 383,
            payload={
                "document_id": "document-B",
                "text": "YOLO is used for object detection.",
                "page_number": 2,
                "chunk_index": 0,
            },
        ),
    ]

    store.add(points)

    results = store.search(
        query_vector=[1.0] + [0.0] * 383,
        document_id="document-A",
        limit=5,
    )

    assert len(results) == 1
    assert results[0].document_id == "document-A"