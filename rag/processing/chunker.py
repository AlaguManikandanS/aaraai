def chunk_documents(pages, chunk_size=1000, overlap=150):
    if chunk_size <= 0:
        raise ValueError("chunk_size must be greater than 0")

    if overlap < 0:
        raise ValueError("overlap cannot be negative")

    if overlap >= chunk_size:
        raise ValueError("overlap must be smaller than chunk_size")

    chunks = []
    chunk_index = 0

    for page in pages:
        text = page["text"].strip()

        if not text:
            continue

        paragraphs = [
            paragraph.strip()
            for paragraph in text.split("\n\n")
            if paragraph.strip()
        ]

        current_chunk = ""

        for paragraph in paragraphs:

            # Handle paragraphs larger than chunk_size
            if len(paragraph) > chunk_size:
                if current_chunk:
                    chunks.append({
                        "chunk_index": chunk_index,
                        "page_number": page["page_number"],
                        "text": current_chunk,
                    })

                    chunk_index += 1
                    current_chunk = ""

                start = 0

                while start < len(paragraph):
                    end = start + chunk_size

                    chunk_text = paragraph[start:end]

                    chunks.append({
                        "chunk_index": chunk_index,
                        "page_number": page["page_number"],
                        "text": chunk_text,
                    })

                    chunk_index += 1

                    start = end - overlap

                continue

            if not current_chunk:
                current_chunk = paragraph
                continue

            candidate = current_chunk + "\n\n" + paragraph

            if len(candidate) <= chunk_size:
                current_chunk = candidate
            else:
                chunks.append({
                    "chunk_index": chunk_index,
                    "page_number": page["page_number"],
                    "text": current_chunk,
                })

                chunk_index += 1

                overlap_text = ""

                if overlap > 0:
                    overlap_start = max(0, len(current_chunk) - overlap)

                    while overlap_start > 0 and not current_chunk[overlap_start].isspace():
                        overlap_start -= 1

                    overlap_text = current_chunk[overlap_start:].strip()

                current_chunk = overlap_text + "\n\n" + paragraph

        if current_chunk:
            chunks.append({
                "chunk_index": chunk_index,
                "page_number": page["page_number"],
                "text": current_chunk,
            })

            chunk_index += 1

    return chunks