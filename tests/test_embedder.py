import pytest

from rag.processing.embedder import EmbeddingModel


def test_embedding_model_generates_embeddings():
    embedder = EmbeddingModel()

    texts = [
        "Deep learning is useful.",
        "Neural networks are powerful.",
    ]

    embeddings = embedder.encode(texts)

    assert len(embeddings) == 2
    assert len(embeddings[0]) == 384
    assert len(embeddings[1]) == 384


def test_encode_requires_list():
    embedder = EmbeddingModel()

    with pytest.raises(TypeError):
        embedder.encode("Deep learning")


def test_encode_requires_strings():
    embedder = EmbeddingModel()

    with pytest.raises(TypeError):
        embedder.encode(["Deep learning", 123])


def test_embedding_model_exposes_dimension():
    embedder = EmbeddingModel()

    assert embedder.dimension == 384