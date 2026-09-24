from rest_framework.decorators import api_view, parser_classes
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework import status

from rag.pipeline.ingestion_pipeline import IngestionPipeline
from rag.pipeline.rag_pipeline import RAGPipeline

from .models import Document
from .serializers import (
    DocumentUploadSerializer,
    QuestionSerializer,
)

@api_view(["GET"])
def health_check(request):
    return Response(
        {
            "status": "ok",
            "service": "aaraai",
        }
    )


@api_view(["POST"])
@parser_classes([MultiPartParser, FormParser])
def upload_document(request):
    serializer = DocumentUploadSerializer(
        data=request.data
    )

    serializer.is_valid(
        raise_exception=True
    )

    uploaded_file = serializer.validated_data["file"]

    document = Document.objects.create(
        file=uploaded_file,
        status="processing",
    )

    pipeline = IngestionPipeline()

    try:
        result = pipeline.ingest(
            pdf_path=document.file.path,
            document_id=str(document.id),
        )

        document.pages = result["pages"]
        document.chunks = result["chunks"]
        document.status = "ready"
        document.save(
            update_fields=[
                "pages",
                "chunks",
                "status",
            ]
        )

    except Exception:
        document.status = "failed"
        document.save(
            update_fields=["status"]
        )

        raise

    return Response(
        {
            "document_id": str(document.id),
            "filename": document.file.name,
            "status": document.status,
            "pages": document.pages,
            "chunks": document.chunks,
        },
        status=status.HTTP_201_CREATED,
    )

@api_view(["POST"])
def ask_question(request):
    serializer = QuestionSerializer(
        data=request.data
    )

    serializer.is_valid(
        raise_exception=True
    )

    question = serializer.validated_data["question"]
    document_id = serializer.validated_data["document_id"]

    try:
        document = Document.objects.get(
            id=document_id
        )
    except Document.DoesNotExist:
        return Response(
            {
                "error": "Document not found."
            },
            status=status.HTTP_404_NOT_FOUND,
        )

    if document.status != "ready":
        return Response(
            {
                "error": "Document is not ready for questions.",
                "status": document.status,
            },
            status=status.HTTP_400_BAD_REQUEST,
        )

    pipeline = RAGPipeline()

    result = pipeline.ask(
        question=question,
        document_id=document_id,
    )

    return Response(result)