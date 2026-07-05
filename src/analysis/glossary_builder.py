import json
from openai import OpenAI
from src.config import client


class GlossaryBuilder:
    def __init__(self, model: str = "gpt-5"):
        self.model = model

    def build_glossary(self, text: str) -> dict:
        response = client.responses.create(
            model=self.model,
            input=[
                {
                    "role": "system",
                    "content": (
                        "Extract all important proper nouns, fantasy terms, "
                        "and world-specific concepts. "
                        "Return ONLY valid JSON in this format:\n"
                        "{\n"
                        '  "terms": {\n'
                        '    "Hungarian term": "English term"\n'
                        "  }\n"
                        "}"
                    )
                },
                {
                    "role": "user",
                    "content": text
                }
            ]
        )

        return json.loads(response.output_text)