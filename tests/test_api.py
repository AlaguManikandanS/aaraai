from django.urls import reverse
from rest_framework.test import APIClient

import pytest

from api.models import Document

import io

from django.core.files.uploadedfile import SimpleUploadedFile


@pytest.mark.django_db
def test_health_check():
    client = APIClient()

    response = client.get("/api/health/")

    assert response.status_code == 200
    assert response.data["status"] == "ok"
    assert response.data["service"] == "aaraai"


@pytest.mark.django_db
def test_question_returns_404_for_missing_document():
    client = APIClient()

    response = client.post(
        "/api/questions/",
        {
            "document_id": "00000000-0000-0000-0000-000000000000",
            "question": "What is this paper about?",
        },
        format="json",
    )

    assert response.status_code == 404
    assert response.data["error"] == "Document not found."


@pytest.mark.django_db
def test_question_rejects_document_that_is_not_ready():
    document = Document.objects.create(
        status="processing",
    )

    client = APIClient()

    response = client.post(
        "/api/questions/",
        {
            "document_id": str(document.id),
            "question": "What is this paper about?",
        },
        format="json",
    )

    assert response.status_code == 400
    assert response.data["error"] == (
        "Document is not ready for questions."
    )
    assert response.data["status"] == "processing"


@pytest.mark.django_db
def test_question_returns_rag_answer_for_ready_document(monkeypatch):
    document = Document.objects.create(
        status="ready",
        pages=8,
        chunks=44,
    )

    class FakeRAGPipeline:
        def __init__(self):
            pass

        def ask(self, question, document_id):
            assert question == "What model does Agam use?"
            assert document_id == str(document.id)

            return {
                "answer": "Agam uses a fine-tuned BERT model. [Page 5]",
                "sources": [
                    {
                        "page_number": 5,
                        "chunk_index": 26,
                        "score": 0.91,
                    }
                ],
            }

    monkeypatch.setattr(
        "api.views.RAGPipeline",
        FakeRAGPipeline,
    )

    client = APIClient()

    response = client.post(
        "/api/questions/",
        {
            "document_id": str(document.id),
            "question": "What model does Agam use?",
        },
        format="json",
    )

    assert response.status_code == 200
    assert response.data["answer"] == (
        "Agam uses a fine-tuned BERT model. [Page 5]"
    )
    assert response.data["sources"][0]["page_number"] == 5

@pytest.mark.django_db
def test_list_documents_returns_documents():
    document = Document.objects.create(
        status="ready",
        pages=8,
        chunks=44,
    )

    client = APIClient()

    response = client.get("/api/documents/")

    assert response.status_code == 200
    assert len(response.data) == 1
    assert response.data[0]["document_id"] == str(document.id)
    assert response.data[0]["status"] == "ready"
    assert response.data[0]["pages"] == 8
    assert response.data[0]["chunks"] == 44


@pytest.mark.django_db
def test_document_detail_returns_document():
    document = Document.objects.create(
        status="ready",
        pages=8,
        chunks=44,
    )

    client = APIClient()

    response = client.get(
        f"/api/documents/{document.id}/"
    )

    assert response.status_code == 200
    assert response.data["document_id"] == str(document.id)
    assert response.data["status"] == "ready"
    assert response.data["pages"] == 8
    assert response.data["chunks"] == 44


@pytest.mark.django_db
def test_document_detail_returns_404_for_missing_document():
    client = APIClient()

    response = client.get(
        "/api/documents/"
        "00000000-0000-0000-0000-000000000000/"
    )

    assert response.status_code == 404
    assert response.data["error"] == "Document not found."

@pytest.mark.django_db
def test_upload_document_success(monkeypatch):
    class FakeIngestionPipeline:
        def ingest(self, pdf_path, document_id):
            return {
                "pages": 8,
                "chunks": 44,
            }

    monkeypatch.setattr(
        "api.views.IngestionPipeline",
        FakeIngestionPipeline,
    )

    pdf_file = SimpleUploadedFile(
        "research.pdf",
        b"%PDF-1.4 fake pdf content",
        content_type="application/pdf",
    )

    client = APIClient()

    response = client.post(
        "/api/documents/upload/",
        {"file": pdf_file},
        format="multipart",
    )

    assert response.status_code == 201
    assert response.data["status"] == "ready"
    assert response.data["pages"] == 8
    assert response.data["chunks"] == 44

    document = Document.objects.get(id=response.data["document_id"])

    assert document.status == "ready"
    assert document.pages == 8
    assert document.chunks == 44


@pytest.mark.django_db
def test_upload_document_marks_failed_when_ingestion_fails(monkeypatch):
    class FakeIngestionPipeline:
        def ingest(self, pdf_path, document_id):
            raise RuntimeError("Ingestion failed")

    monkeypatch.setattr(
        "api.views.IngestionPipeline",
        FakeIngestionPipeline,
    )

    pdf_file = SimpleUploadedFile(
        "research.pdf",
        b"%PDF-1.4 fake pdf content",
        content_type="application/pdf",
    )

    client = APIClient(raise_request_exception=False)

    response = client.post(
        "/api/documents/upload/",
        {"file": pdf_file},
        format="multipart",
    )

    assert response.status_code == 500
    assert response.data["error"] == "Document processing failed."
    assert response.data["status"] == "failed"

    documents = Document.objects.all()

    assert documents.count() == 1

    document = documents.first()

    assert document.status == "failed"