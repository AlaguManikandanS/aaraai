from django.urls import path

from .views import (
    health_check,
    upload_document,
    ask_question,
)


urlpatterns = [
    path("health/", health_check),
    path("documents/", upload_document),
    path("questions/", ask_question),
]