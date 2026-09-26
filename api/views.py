from rest_framework.decorators import api_view, parser_classes
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework import status

from rag.pipeline.rag_pipeline import RAGPipeline

from .models import Document
from .serializers import (
    DocumentSerializer,
    DocumentUploadSerializer,
    QuestionSerializer,
)

from .tasks import process_document


@api_view(["GET"])
def health_check(request):
    return Response(
        {
            "status": "ok",
            "service": "aaraai",
        }
    )

@api_view(["GET"])
def list_documents(request):
    documents = Document.objects.all().order_by("-created_at")

    serializer = DocumentSerializer(
        documents,
        many=True,
    )

    return Response(serializer.data)


@api_view(["POST"])
@parser_classes([MultiPartParser, FormParser])
def upload_document(request):
    serializer = DocumentUploadSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    uploaded_file = serializer.validated_data["file"]

    document = Document.objects.create(
        file=uploaded_file,
        status="processing",
    )

    process_document.delay(str(document.id))

    return Response(
        {
            "document_id": str(document.id),
            "filename": document.file.name,
            "status": document.status,
            "pages": document.pages,
            "chunks": document.chunks,
        },
        status=status.HTTP_202_ACCEPTED,
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

@api_view(["GET"])
def document_detail(request, document_id):
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

    serializer = DocumentSerializer(document)

    return Response(serializer.data)