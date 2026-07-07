from typing import List, Dict, Any


class Chunker:
    def __init__(self, max_words: int = 1200):
        self.max_words = max_words

    # -----------------------
    # STRUCTURED CHUNKING (FIXED)
    # -----------------------
    def create_chunks_structured(self, scene: list[dict]) -> List[list[dict]]:

        chunks = []
        current_chunk = []
        current_word_count = 0

        for p in scene:

            text = p["text"]
            word_count = len(text.split())

            style = p.get("style", "Normal")

            # -----------------------
            # HEADING → FORCE NEW CHUNK
            # -----------------------
            if style.startswith("Heading"):

                if current_chunk:
                    chunks.append(current_chunk)
                    current_chunk = []
                    current_word_count = 0

                # heading is its own chunk BUT KEEP FULL STRUCTURE
                chunks.append([p])
                continue

            # -----------------------
            # TOO LARGE PARAGRAPH
            # -----------------------
            if word_count > self.max_words:

                if current_chunk:
                    chunks.append(current_chunk)
                    current_chunk = []
                    current_word_count = 0

                chunks.append([p])
                continue

            # -----------------------
            # CHUNK LIMIT CHECK
            # -----------------------
            if current_word_count + word_count > self.max_words:

                chunks.append(current_chunk)
                current_chunk = [p]
                current_word_count = word_count

            else:
                current_chunk.append(p)
                current_word_count += word_count

        # -----------------------
        # FINAL FLUSH
        # -----------------------
        if current_chunk:
            chunks.append(current_chunk)

        return chunks