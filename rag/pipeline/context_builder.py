from rag.retrieval.models import RetrievedChunk


def build_context(chunks: list[RetrievedChunk]) -> str:
    """
    Convert retrieved chunks into formatted context for the LLM.

    Each chunk includes its page number so that the generated
    answer can later reference the source page.
    """

    if not chunks:
        return ""

    context_parts = []

    for chunk in chunks:
        context_parts.append(
            f"[Page {chunk.page_number}]\n"
            f"{chunk.text}"
        )

    return "\n\n".join(context_parts)