import json
from src.config import client


class POVAnalyzer:

    def analyze_chunks(self, chunks):

        results = []

        for i, chunk in enumerate(chunks):

            print(f"Analyzing POV for chunk {i}...")

            response = client.responses.create(
                model="gpt-5",
                input=self._build_prompt(chunk)
            )

            try:
                result = json.loads(response.output_text)

            except Exception:

                result = {
                    "pov": "Unknown",
                    "reason": "Could not parse model output."
                }

            result["chunk"] = i

            results.append(result)

        return results


    def group_from_analysis(self, chunks, analysis):

        grouped = {}

        for item in analysis:

            pov = item["pov"]

            if pov not in grouped:
                grouped[pov] = []

            grouped[pov].append(
                chunks[item["chunk"]]
            )

        return grouped


    def _build_prompt(self, chunk):

        return f"""
You are an expert literary editor.

Determine the point-of-view (POV) character of the following passage.

The POV character is the one whose thoughts, feelings,
perceptions and internal experiences the narration follows. 
Use the exact name of the viewpoint character as it appears in the text.

Rules:

- Return ONLY valid JSON.
- Use ONLY the character's name.
- If there is no clear POV, return "Unknown".

Return exactly:

{{
    "pov": "...",
    "reason": "..."
}}

TEXT:

{chunk}
"""