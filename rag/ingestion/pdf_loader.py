import fitz


def load_pdf(pdf_path):
    """
    Extract text from a PDF page by page.

    Args:
        pdf_path: Path to the PDF file.

    Returns:
        A list of dictionaries containing page numbers and extracted text.
    """

    document = fitz.open(pdf_path)

    pages = []

    for page_index, page in enumerate(document):
        text = page.get_text()

        text = " ".join(text.split())

        pages.append({
            "page_number": page_index + 1,
            "text": text,
        })

    document.close()

    return pages