import pytest

from rag.pipeline.summary_prompt_builder import build_summary_prompt


def test_build_summary_prompt_contains_context():
    context = "[Page 1]\nThis paper proposes an AI-based learning system."

    prompt = build_summary_prompt(context)

    assert context in prompt
    assert "OVERVIEW:" in prompt
    assert "PROBLEM:" in prompt
    assert "METHODOLOGY:" in prompt
    assert "KEY FINDINGS:" in prompt
    assert "LIMITATIONS:" in prompt


def test_build_summary_prompt_rejects_empty_context():
    with pytest.raises(ValueError, match="context cannot be empty"):
        build_summary_prompt("")