def build_prompt(question: str, context: str) -> str:
    """
    Build a grounded prompt for the research-paper LLM.

    The LLM is instructed to answer using only the retrieved
    context and to reference page numbers when possible.
    """

    if not question.strip():
        raise ValueError("question cannot be empty")

    if not context.strip():
        raise ValueError("context cannot be empty")

    prompt = f"""You are Aaraai, an AI assistant for understanding research papers.

Answer the user's question using only the provided research-paper context.

Rules:
1. Do not use information that is not present in the provided context.
2. If the answer cannot be found in the context, say that the information
   could not be found in the paper.
3. Give a clear and concise answer.
4. Mention the relevant page number when possible.
5. Do not invent facts, citations, or references.

RESEARCH PAPER CONTEXT:
{context}

USER QUESTION:
{question}

ANSWER:
"""

    return prompt