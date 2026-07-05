import json
from openai import OpenAI
from src.config import client

class StyleBuilder:
    def build_style(
        self,
        source_text: str,
        reference_translation: str | None = None
    ):

        if reference_translation:
            prompt = self._build_reference_prompt(
                source_text,
                reference_translation
            )
        else:
            prompt = self._build_standard_prompt(source_text)

        response = client.responses.create(
            model="gpt-5.5",
            input=prompt
        )

        content = response.output_text

        try:
            return json.loads(content)
        except json.JSONDecodeError:
            print("⚠ Could not parse style profile JSON.")
            return {"raw_response": content}

    # ------------------------------------------------------
    # Standard style analysis
    # ------------------------------------------------------

    def _build_standard_prompt(self, source_text):

        return f"""
You are an expert literary editor.

Analyze the writing style of the following novel excerpt.

Describe:

- narrative voice
- sentence length
- pacing
- dialogue style
- descriptive density
- emotional intensity
- figurative language
- vocabulary
- tone

Return ONLY valid JSON with the following structure:
{{
  "sentence_length": "...",
  "narrative_voice": "...",
  "dialogue_style": "...",
  "tone": "...",
  "pacing": "...",
  "vocabulary": "...",
  "figurative_language": "...",
  "proper_nouns": "...",
  "capitalization": "...",
  "notes": "..."
}}

TEXT:

{source_text}
"""

    # ------------------------------------------------------
    # Reference translation analysis
    # ------------------------------------------------------

    def _build_reference_prompt(
        self,
        source_text,
        reference_translation
    ):

        return f"""
You are an expert literary translator.

You are given:

1. The original Hungarian text.
2. A professionally edited English translation of the same passage.

Do NOT translate anything.

Your task is to infer the translation style that should be consistently used for the rest of the novel.

Analyze:

- sentence rhythm
- sentence length
- dialogue style
- narrative distance
- descriptive density
- vocabulary level
- figurative language
- tone
- pacing
- tense usage
- handling of idioms
- capitalization conventions
- punctuation preferences
- treatment of names and fantasy terms

Return ONLY valid JSON with the following structure:
{{
  "sentence_length": "...",
  "narrative_voice": "...",
  "dialogue_style": "...",
  "tone": "...",
  "pacing": "...",
  "vocabulary": "...",
  "figurative_language": "...",
  "proper_nouns": "...",
  "capitalization": "...",
  "notes": "..."
}}

ORIGINAL (Hungarian)

------------------------

{source_text}

------------------------

REFERENCE TRANSLATION (English)

------------------------

{reference_translation}
"""