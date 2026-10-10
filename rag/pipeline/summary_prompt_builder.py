
SUMMARY_SCHEMA = {
    "type": "object",
    "properties": {
        "OVERVIEW": {"type": "string"},
        "PROBLEM": {"type": "string"},
        "METHODOLOGY": {"type": "string"},
        "KEY FINDINGS": {
            "type": "array",
            "items": {"type": "string"},
        },
        "LIMITATIONS": {
            "type": "array",
            "items": {"type": "string"},
        },
    },
    "required": [
        "OVERVIEW",
        "PROBLEM",
        "METHODOLOGY",
        "KEY FINDINGS",
        "LIMITATIONS",
    ],
    "additionalProperties": False,
}


def build_summary_prompt(context: str) -> str:
    """
    Build a grounded prompt for generating a structured research-paper overview.

    The LLM must use only the provided research-paper context.
    """

    if not context.strip():
        raise ValueError("context cannot be empty")

    prompt = f"""You are Aaraai, an AI assistant for understanding research papers.

Your task is to create a structured overview of the research paper.

IMPORTANT RULES:

1. Use ONLY information contained in the research-paper context below.
2. Do NOT use outside knowledge.
3. Do NOT invent facts, results, methods, or conclusions.
4. You MUST output ALL FIVE sections.
5. Never skip a section.
6. If information for a section is not available, write exactly:
   Not available in the provided context.
7. Keep each section concise and informative.
8. Do NOT use Markdown formatting such as **, ##, or ###.
9. Do NOT add citations or page numbers.
10. Use the exact section names and order shown below.
11. For KEY FINDINGS, use 2 to 4 bullet points.
12. For LIMITATIONS, use 2 to 4 bullet points.
13. Each bullet must start with "- ".
14. Do not put bullets in the OVERVIEW, PROBLEM, or METHODOLOGY sections.
15. Do not create sections such as Title, Authors, Abstract,
    Keywords, Introduction, Methods, Results, or References.
16. Do not reproduce the paper's original structure.
17. Your entire response must contain only the five required
    sections and their content.
18. Do not include placeholder text such as [Authors' Names].
19. Under KEY FINDINGS, report only findings explicitly
    supported by the context. Do not claim clinical validation
    or strong model performance unless the context provides evidence.


OUTPUT FORMAT:

Return only a valid JSON object matching the supplied schema.

- OVERVIEW: A concise paragraph explaining the paper.
- PROBLEM: A concise paragraph describing the problem addressed.
- METHODOLOGY: A concise paragraph describing the approach.
- KEY FINDINGS: An array of 2 to 4 evidence-supported findings.
- LIMITATIONS: An array of 2 to 4 evidence-supported limitations.

Use only claims supported by the research-paper context.
Do not invent results, performance metrics, or clinical validation.
If information is missing, explicitly state that it is not available.
Do not include Markdown or additional sections.


RESEARCH PAPER CONTEXT:

{context}

Now produce the PAPER OVERVIEW using exactly the required format above.
"""

    return prompt