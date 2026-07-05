class MarkupConverter:
    """
    Converts DOCX formatting into internal markup structure.

    IMPORTANT:
    - Does NOT flatten structure into a single string
    - Preserves runs as atomic units
    - Separates paragraph metadata from inline markup
    """

    def to_markup(self, paragraph):

        # -------------------------
        # PARAGRAPH STYLE (META)
        # -------------------------

        style_name = (
            paragraph.style.name
            if paragraph.style
            else "Normal"
        )

        # -------------------------
        # INLINE RUN PROCESSING
        # -------------------------

        runs = []

        for run in paragraph.runs:

            text = run.text

            if not text:
                continue

            tokens = []

            # apply inline markers per run (no join yet)
            if run.bold:
                tokens.append("⟦BOLD⟧")
            if run.italic:
                tokens.append("⟦ITALIC⟧")
            if run.underline:
                tokens.append("⟦UNDERLINE⟧")

            tokens.append(text)

            if run.bold:
                tokens.append("⟦/BOLD⟧")
            if run.italic:
                tokens.append("⟦/ITALIC⟧")
            if run.underline:
                tokens.append("⟦/UNDERLINE⟧")

            runs.append(tokens)

        # -------------------------
        # RETURN STRUCTURED FORMAT
        # -------------------------

        return {
            "style": style_name,
            "runs": runs
        }