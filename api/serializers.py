from rest_framework import serializers
from .models import Document


class DocumentUploadSerializer(serializers.Serializer):
    file = serializers.FileField()

    def validate_file(self, value):
        if not value.name.lower().endswith(".pdf"):
            raise serializers.ValidationError(
                "Only PDF files are supported."
            )

        return value


class QuestionSerializer(serializers.Serializer):
    document_id = serializers.CharField()
    question = serializers.CharField()

    def validate_document_id(self, value):
        if not value.strip():
            raise serializers.ValidationError(
                "document_id cannot be empty."
            )

        return value

    def validate_question(self, value):
        if not value.strip():
            raise serializers.ValidationError(
                "question cannot be empty."
            )

        return value

class DocumentSerializer(serializers.ModelSerializer):
    document_id = serializers.UUIDField(
        source="id"
    )

    filename = serializers.CharField(
        source="file.name",
        read_only=True,
    )

    class Meta:
        model = Document
        fields = [
            "document_id",
            "filename",
            "status",
            "pages",
            "chunks",
            "created_at",
        ]