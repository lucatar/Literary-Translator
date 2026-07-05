from docx import Document


class DocumentParser:
    def __init__(self, file_path: str):
        self.file_path = file_path

    def read(self) -> list[str]:
        """
        BACKWARD COMPATIBLE:
        pipeline továbbra is ezt használja
        """
        doc = Document(self.file_path)

        paragraphs = []

        for p in doc.paragraphs:
            text = p.text

            if text and text.strip():
                paragraphs.append(text.strip())

        return paragraphs

    def read_structured(self):
        """
        NEW: run-level capture (nem breaking change)
        """
        doc = Document(self.file_path)

        structured = []

        for p in doc.paragraphs:

            runs = []
            full_text = ""

            for r in p.runs:

                if not r.text:
                    continue

                runs.append({
                    "text": r.text,
                    "bold": bool(r.bold),
                    "italic": bool(r.italic),
                    "underline": bool(r.underline),
                })

                full_text += r.text

            if full_text.strip():
                structured.append({
                    "text": full_text.strip(),
                    "runs": runs,
                    "style": p.style.name if p.style else "Normal"
                })

        return structured