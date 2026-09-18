import fitz

from rag.ingestion.pdf_loader import load_pdf


def create_test_pdf(path):
    document = fitz.open()

    page1 = document.new_page()
    page1.insert_text((72, 72), "Aaraai test page one")

    page2 = document.new_page()
    page2.insert_text((72, 72), "Aaraai test page two")

    document.save(path)
    document.close()


def test_load_pdf_extracts_pages(tmp_path):
    pdf_path = tmp_path / "test.pdf"

    create_test_pdf(pdf_path)

    pages = load_pdf(pdf_path)

    assert len(pages) == 2
    assert pages[0]["page_number"] == 1
    assert pages[1]["page_number"] == 2
    assert "Aaraai test page one" in pages[0]["text"]
    assert "Aaraai test page two" in pages[1]["text"]