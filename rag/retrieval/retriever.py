from rag.retrieval.similarity import cosine_similarity


def retrieve_top_k(query_embedding, chunk_embeddings, chunks, k=3):
    if k <= 0:
        raise ValueError("k must be greater than 0")

    if len(chunk_embeddings) != len(chunks):
        raise ValueError("chunk_embeddings and chunks must have the same length")

    results = []

    for embedding, chunk in zip(chunk_embeddings, chunks):
        score = cosine_similarity(query_embedding, embedding)

        results.append({
            "score": score,
            "chunk": chunk,
        })

    results.sort(key=lambda result: result["score"], reverse=True)

    return results[:k]