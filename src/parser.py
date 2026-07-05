from docx import Document


class DocumentParser:
    def __init__(self, file_path: str):
        self.file_path = file_path

    def read(self) -> list[str]:
        """
        Returns clean paragraph strings.
        Compatible with string-based pipeline.
        """

        doc = Document(self.file_path)

        paragraphs = []

        for p in doc.paragraphs:

            text = p.text

            if not text:
                continue

            text = text.strip()

            if text:
                paragraphs.append(text)

        return paragraphs