from src.config import client


class Translator:
    def __init__(self, model: str = "gpt-5"):
        self.model = model

    def translate_chunk(self, chunk: str, style: dict, glossary: dict) -> str:
        response = client.responses.create(
            model=self.model,
            input=[
                {
                    "role": "system",
                    "content": f"""
You are a professional literary translator.

CRITICAL RULES (must follow exactly):
1. You MUST follow the STYLE GUIDE.
2. You MUST use the GLOSSARY consistently.
3. Do NOT introduce new terminology.
4. Do NOT paraphrase character names or world terms.
5. Maintain consistency across the entire book.
6. Do NOT add any content that is not present in the original text.
7. Do NOT change the meaning of the original text.
8. Do NOT translate idioms or phrases literally if they do not make sense in the target language. Replace them with culturally appropriate equivalents.
9. Refrain from em dashes unless it is absolutely necessary for the meaning of the sentence.
10. Preserve all markup text exactly as it appears in the source text.

STYLE GUIDE (JSON):
{style}

GLOSSARY (JSON):
{glossary}
"""
                },
                {
                    "role": "user",
                    "content": chunk
                }
            ]
        )

        return response.output_text