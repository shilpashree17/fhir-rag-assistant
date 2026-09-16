import os
from typing import Optional


class LLMClient:
    def __init__(self, model: Optional[str] = None):
        self.model = model or os.getenv("OPENAI_MODEL", "gpt-4o-mini")

    def generate(self, prompt: str) -> str:
        raise NotImplementedError("Implement your LLM provider integration here.")
