import pytest

from rag.retrieval.retriever import retrieve_top_k


def test_retrieve_top_k_returns_most_similar_chunks():
    query_embedding = [1, 0]

    chunk_embeddings = [
        [0, 1],
        [1, 0],
        [0.8, 0.6],
    ]

    chunks = [
        {
            "chunk_index": 0,
            "page_number": 1,
            "text": "Unrelated content",
        },
        {
            "chunk_index": 1,
            "page_number": 2,
            "text": "Most relevant content",
        },
        {
            "chunk_index": 2,
            "page_number": 3,
            "text": "Somewhat relevant content",
        },
    ]

    results = retrieve_top_k(
        query_embedding,
        chunk_embeddings,
        chunks,
        k=2,
    )

    assert len(results) == 2
    assert results[0]["chunk"]["chunk_index"] == 1
    assert results[1]["chunk"]["chunk_index"] == 2
    assert results[0]["score"] > results[1]["score"]


def test_retrieve_top_k_rejects_invalid_k():
    with pytest.raises(ValueError):
        retrieve_top_k(
            [1, 0],
            [[1, 0]],
            [{"chunk_index": 0}],
            k=0,
        )


def test_retrieve_top_k_rejects_mismatched_lengths():
    with pytest.raises(ValueError):
        retrieve_top_k(
            [1, 0],
            [[1, 0]],
            [],
            k=1,
        )