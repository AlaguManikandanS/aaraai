import pytest

from django.core.files.uploadedfile import SimpleUploadedFile

from api.models import Document
from api.tasks import process_document


@pytest.mark.django_db
def test_process_document_marks_document_ready(monkeypatch):
    pdf_file = SimpleUploadedFile(
        "research.pdf",
        b"%PDF-1.4 fake pdf content",
        content_type="application/pdf",
    )

    document = Document.objects.create(
        file=pdf_file,
        status="processing",
    )

    class FakeIngestionPipeline:
        def ingest(self, pdf_path, document_id):
            assert document_id == str(document.id)
            assert pdf_path.endswith(".pdf")

            return {
                "pages": 8,
                "chunks": 44,
            }

    monkeypatch.setattr(
        "api.tasks.IngestionPipeline",
        FakeIngestionPipeline,
    )

    process_document.run(str(document.id))

    document.refresh_from_db()

    assert document.status == "ready"
    assert document.pages == 8
    assert document.chunks == 44


@pytest.mark.django_db
def test_process_document_marks_document_failed(monkeypatch):
    pdf_file = SimpleUploadedFile(
        "research.pdf",
        b"%PDF-1.4 fake pdf content",
        content_type="application/pdf",
    )

    document = Document.objects.create(
        file=pdf_file,
        status="processing",
    )

    class FakeIngestionPipeline:
        def ingest(self, pdf_path, document_id):
            raise RuntimeError("Ingestion failed")

    monkeypatch.setattr(
        "api.tasks.IngestionPipeline",
        FakeIngestionPipeline,
    )

    with pytest.raises(RuntimeError, match="Ingestion failed"):
        process_document.run(str(document.id))

    document.refresh_from_db()

    assert document.status == "failed"