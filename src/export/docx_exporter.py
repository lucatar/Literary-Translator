from docx import Document


class DocxExporter:

    def __init__(self):
        self.doc = Document()

    def add_chunks(self, chunks):

        for chunk in chunks:
            
            # -----------------------
            # BACKWARD SAFE HANDLING
            # -----------------------
            if isinstance(chunk, str):
                self.doc.add_paragraph(chunk)
                continue

            text = chunk.get("text", "")
            style = chunk.get("style", "Normal")

            if not text:
                continue

            # -----------------------
            # PARAGRAPH
            # -----------------------
            p = self.doc.add_paragraph()

            # style only (NO CRASH EVER)
            if style:
                try:
                    p.style = style
                except Exception:
                    p.style = "Normal"

            # -----------------------
            # TEXT ONLY (no runs for now)
            # -----------------------
            #print(text, style)
            p.add_run(text)

    def save(self, output_path: str):
        self.doc.save(output_path)