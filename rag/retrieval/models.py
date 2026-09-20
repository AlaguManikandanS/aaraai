from dataclasses import dataclass


@dataclass
class RetrievedChunk:
    score: float
    document_id: str
    page_number: int
    chunk_index: int
    text: str