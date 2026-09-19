import fitz

from rag.pipeline.ingestion_pipeline import IngestionPipeline
from rag.processing.embedder import EmbeddingModel


def create_test_pdf(path):
    document = fitz.open()

    page1 = document.new_page()
    page1.insert_text(
        (72, 72),
        "The model uses BERT to detect cognitive distortions."
    )

    page2 = document.new_page()
    page2.insert_text(
        (72, 72),
        "The system uses behavioral signals for risk prediction."
    )

    document.save(path)
    document.close()


def test_ingestion_pipeline(tmp_path):
    pdf_path = tmp_path / "test.pdf"

    create_test_pdf(pdf_path)

    pipeline = IngestionPipeline(collection_name="aaraai_test_chunks")

    result = pipeline.ingest(
        str(pdf_path),
        document_id="test-document",
    )

    assert result["document_id"] == "test-document"
    assert result["pages"] == 2
    assert result["chunks"] >= 1