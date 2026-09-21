from rag.retrieval.models import RetrievedChunk


def build_response(
    answer: str,
    retrieved_chunks: list[RetrievedChunk],
):
    """
    Build the final RAG response.

    The answer comes from the LLM, while source information
    comes directly from retrieved document metadata.
    """

    answer = answer.strip()

    pages = []

    for chunk in retrieved_chunks:
        if chunk.page_number not in pages:
            pages.append(chunk.page_number)

    citation = " ".join(
        f"[Page {page}]"
        for page in pages
    )

    if citation:
        answer = f"{answer} {citation}".strip()

    sources = [
        {
            "page_number": chunk.page_number,
            "chunk_index": chunk.chunk_index,
            "score": chunk.score,
        }
        for chunk in retrieved_chunks
    ]

    return {
        "answer": answer,
        "sources": sources,
    }