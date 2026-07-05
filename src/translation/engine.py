class TranslationEngine:

    def __init__(self, translator, cache, config):
        self.translator = translator
        self.cache = cache
        self.config = config

    def translate_document(
        self,
        chunks,            # <-- STRING chunks
        style_profiles,
        pov_analysis,
        glossary
    ):

        translated_chunks = []

        for i, chunk in enumerate(chunks):

            # -----------------------
            # CACHE
            # -----------------------

            cached = self.cache.get_translated_chunk(i)

            if cached:
                print(f"Chunk {i} loaded from cache")
                translated_chunks.append(cached["text"])
                continue

            print(f"Translating chunk {i}")

            # -----------------------
            # STYLE SELECTION
            # -----------------------

            pov = pov_analysis[i]["pov"]
            style = style_profiles.get(pov)

            if style is None:
                print(f"Warning: missing style for POV '{pov}', using fallback.")
                style = next(iter(style_profiles.values()))

            # -----------------------
            # TRANSLATION (STRING IN → STRING OUT)
            # -----------------------

            translated = self.translator.translate_chunk(
                chunk,
                style=style,
                glossary=glossary
            )

            # -----------------------
            # CACHE SAVE
            # -----------------------

            self.cache.save_translated_chunk(
                i,
                {
                    "id": i,
                    "text": translated
                }
            )

            translated_chunks.append(translated)

        return translated_chunks