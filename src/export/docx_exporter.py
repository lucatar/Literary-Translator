from docx import Document


class DocxExporter:

    def __init__(self):
        self.doc = Document()

    def add_chunks(self, chunks):

        for chunk in chunks:

            paragraphs = chunk.split("\n")

            for text in paragraphs:

                text = text.strip()

                if text:
                    self._add_paragraph(text)

    def _add_paragraph(self, text):

        self.doc.add_paragraph(text)

    def save(self, output_path: str):
        self.doc.save(output_path)