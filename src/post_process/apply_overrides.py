import json
import re
from docx import Document
import os


def apply_translation_overrides(output_docx, knowledge_base_dir):

    overrides_path = os.path.join(
        knowledge_base_dir,
        "translation_overrides.json"
    )

    if not os.path.exists(overrides_path):
        return

    with open(overrides_path, "r", encoding="utf-8") as f:
        overrides = json.load(f)

    doc = Document(output_docx)

    for para in doc.paragraphs:

        text = para.text

        for old, new in overrides.items():

            if old == new:
                continue

            pattern = re.compile(
                rf"\b{re.escape(old)}\b"
            )

            text = pattern.sub(new, text)

        para.text = text

    doc.save(output_docx)

    print("Translation overrides applied.")
    