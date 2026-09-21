import pytest

from rag.generation.llm_client import LLMClient


def test_llm_client_uses_default_configuration(monkeypatch):
    monkeypatch.delenv("OLLAMA_URL", raising=False)
    monkeypatch.delenv("OLLAMA_MODEL", raising=False)

    client = LLMClient()

    assert client.base_url == "http://localhost:11434"
    assert client.model == "qwen2.5:7b-instruct-q4_K_M"


def test_llm_client_rejects_empty_prompt():
    client = LLMClient()

    with pytest.raises(ValueError, match="prompt cannot be empty"):
        client.generate("")


def test_llm_client_generates_response(monkeypatch):
    class FakeResponse:
        def raise_for_status(self):
            pass

        def json(self):
            return {
                "response": "RAG retrieves relevant context before generation."
            }

    def fake_post(*args, **kwargs):
        assert args[0] == "http://localhost:11434/api/generate"

        assert kwargs["json"]["model"] == "qwen2.5:7b-instruct-q4_K_M"
        assert kwargs["json"]["prompt"] == "What is RAG?"
        assert kwargs["json"]["stream"] is False

        return FakeResponse()

    monkeypatch.setattr(
        "rag.generation.llm_client.requests.post",
        fake_post,
    )

    client = LLMClient()

    result = client.generate("What is RAG?")

    assert result == "RAG retrieves relevant context before generation."