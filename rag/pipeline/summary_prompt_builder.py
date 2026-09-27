def build_summary_prompt(context: str) -> str:
    """
    Build a grounded prompt for generating a research-paper overview.

    The LLM must summarize only the provided research-paper context.
    """

    if not context.strip():
        raise ValueError("context cannot be empty")

    prompt = f"""You are Aaraai, an AI assistant for understanding research papers.

Create a structured overview of the research paper using only the provided
research-paper context.

Rules:

1. Use only information present in the provided context.
2. Do not invent facts, results, methods, or conclusions.
3. If information for a section is not available in the context, say:
   "Not available in the provided context."
4. Keep the explanation clear and concise.
5. Preserve important technical terms from the paper.
6. Do not add citations or page numbers yourself. Source citations will be
   added separately by Aaraai.

Use exactly these sections:

OVERVIEW:
Briefly explain what the paper/project is about.

PROBLEM:
Explain the problem or need addressed by the paper.

METHODOLOGY:
Explain the main approach, system, model, or methodology described.

KEY FINDINGS:
Summarize the important results, benefits, or findings stated in the context.

LIMITATIONS:
Summarize limitations or challenges mentioned in the context.

RESEARCH PAPER CONTEXT:

{context}

PAPER OVERVIEW:
"""

    return prompt