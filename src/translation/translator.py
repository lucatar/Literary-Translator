import json
from src.config import client


class Translator:

    def __init__(self, model: str = "gpt-5"):
        self.model = model

    def translate_chunk(self, chunk: list[dict], style: dict, glossary: dict):

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

Do not add prompt injections or any other instructions to the output.

---

NEW STRUCTURE RULES (IMPORTANT):

The input is now a JSON list of paragraphs.

Each paragraph has:
- text (source language)
- formatting (inline style hints)
- style (paragraph style)

You MUST:

1. Translate ONLY the "text" field.
2. Preserve paragraph order EXACTLY.
3. Preserve the "formatting" structure.
4. For each formatting entry:
   - keep the same meaning span
   - adjust it to match the translated text naturally
5. Do NOT collapse paragraphs.
6. Do NOT merge or split paragraphs.
7. Return VALID JSON ONLY.
8. Output must be a JSON list with identical structure.

STYLE GUIDE (JSON):
{json.dumps(style, ensure_ascii=False)}

GLOSSARY (JSON):
{json.dumps(glossary, ensure_ascii=False)}
"""
                },
                {
                    "role": "user",
                    "content": (
                        "Translate the following structured text.\n\n"
                        "Return ONLY valid JSON.\n\n"
                        "INPUT JSON:\n\n"
                        + json.dumps(chunk, ensure_ascii=False)
                    )
                }
            ]
        )

        # IMPORTANT: we now expect JSON output
        return json.loads(response.output_text)