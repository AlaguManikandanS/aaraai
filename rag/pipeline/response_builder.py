def build_response(answer, retrieved_chunks):
    sources = [
        {
            "page_number": chunk.page_number,
            "chunk_index": chunk.chunk_index,
            "score": chunk.score,
        }
        for chunk in retrieved_chunks
    ]

    return {
        "answer": answer.strip(),
        "sources": sources,
    }