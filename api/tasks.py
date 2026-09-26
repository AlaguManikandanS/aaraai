from celery import shared_task

from rag.pipeline.ingestion_pipeline import IngestionPipeline

from .models import Document


@shared_task
def process_document(document_id):
    document = Document.objects.get(id=document_id)

    if document.status != "processing":
        return

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
            update_fields=["pages", "chunks", "status"]
        )

    except Exception:
        document.status = "failed"
        document.save(update_fields=["status"])
        raise