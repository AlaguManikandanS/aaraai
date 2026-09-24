from django.urls import reverse
from rest_framework.test import APIClient

import pytest

from api.models import Document


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