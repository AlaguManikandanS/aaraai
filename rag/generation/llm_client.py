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
            "qwen2.5:3b-instruct-q4_K_M",
        )

        self.base_url = base_url or os.getenv(
            "OLLAMA_URL",
            "http://localhost:11434",
        )

    
    def generate(self, prompt: str, output_format=None) -> str:
        if not prompt.strip():
            raise ValueError("prompt cannot be empty")

        payload = {
            "model": self.model,
            "prompt": prompt,
            "stream": False,
            "options": {
                "temperature": 0.1,
                "num_predict": 1000,
                "num_ctx": 8192,
            },
        }

        if output_format is not None:
            payload["format"] = output_format

        response = requests.post(
            f"{self.base_url}/api/generate",
            json=payload,
            timeout=300,
        )

        if not response.ok:
            raise RuntimeError(
                f"Ollama request failed: "
                f"status={response.status_code}, "
                f"body={response.text}"
            )

        data = response.json()
        return data["response"]
