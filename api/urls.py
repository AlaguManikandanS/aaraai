from django.urls import path

from .views import (
    health_check,
    list_documents,
    document_detail,
    upload_document,
    ask_question,
)


urlpatterns = [
    path("health/", health_check),

    path("documents/", list_documents),
    path("documents/upload/", upload_document),
    path(
        "documents/<uuid:document_id>/",
        document_detail,
    ),

    path("questions/", ask_question),
]