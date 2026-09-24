import os

import requests
from dotenv import load_dotenv


load_dotenv()


class LLMClient:
    def __init__(
        self,
        model=None,
        base_url=None,
    ):
        self.model = model or os.getenv(
            "OLLAMA_MODEL",
            "qwen2.5:7b-instruct-q4_K_M",
        )

        self.base_url = base_url or os.getenv(
            "OLLAMA_URL",
            "http://localhost:11434",
        )

    def generate(self, prompt: str) -> str:
        if not prompt.strip():
            raise ValueError("prompt cannot be empty")

        response = requests.post(
            f"{self.base_url}/api/generate",
            json={
                "model": self.model,
                "prompt": prompt,
                "stream": False,
            },
            timeout=120,
        )

        if not response.ok:
            raise RuntimeError(
                f"Ollama request failed: "
                f"status={response.status_code}, "
                f"body={response.text}"
            )
        data = response.json()

        return data["response"]