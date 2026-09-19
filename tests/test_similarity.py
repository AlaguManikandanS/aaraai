from rag.retrieval.similarity import cosine_similarity


def test_identical_vectors_have_similarity_one():
    vector = [1, 2, 3]

    score = cosine_similarity(vector, vector)

    assert abs(score - 1.0) < 1e-6


def test_orthogonal_vectors_have_similarity_zero():
    vector_a = [1, 0]
    vector_b = [0, 1]

    score = cosine_similarity(vector_a, vector_b)

    assert abs(score) < 1e-6


def test_zero_vector_returns_zero():
    vector_a = [0, 0]
    vector_b = [1, 2]

    score = cosine_similarity(vector_a, vector_b)

    assert score == 0.0