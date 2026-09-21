import pytest

from rag.pipeline.prompt_builder import build_prompt


def test_build_prompt_contains_context_and_question():
    context = (
        "[Page 5]\n"
        "Agam uses a fine-tuned BERT model for cognitive distortion detection."
    )

    question = "What model does Agam use?"

    prompt = build_prompt(question, context)

    assert "Agam uses a fine-tuned BERT model" in prompt
    assert "What model does Agam use?" in prompt
    assert "Page 5" in prompt
    assert "provided research-paper context" in prompt


def test_build_prompt_rejects_empty_question():
    with pytest.raises(ValueError, match="question cannot be empty"):
        build_prompt("", "Some context")


def test_build_prompt_rejects_empty_context():
    with pytest.raises(ValueError, match="context cannot be empty"):
        build_prompt("What model is used?", "")