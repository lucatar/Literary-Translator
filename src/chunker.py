from typing import List


class Chunker:
    def __init__(self, max_words: int = 1200):
        self.max_words = max_words

    def create_chunks(self, text: str) -> List[str]:
        paragraphs = text.split("\n")

        chunks = []
        current_chunk = []
        current_word_count = 0

        for paragraph in paragraphs:
            paragraph = paragraph.strip()
            if not paragraph:
                continue

            word_count = len(paragraph.split())

            # ha egy bekezdés túl nagy
            if word_count > self.max_words:
                if current_chunk:
                    chunks.append(" ".join(current_chunk))
                    current_chunk = []
                    current_word_count = 0

                chunks.append(paragraph)
                continue

            # ha túllépi a limitet
            if current_word_count + word_count > self.max_words:
                chunks.append(" ".join(current_chunk))
                current_chunk = [paragraph]
                current_word_count = word_count
            else:
                current_chunk.append(paragraph)
                current_word_count += word_count

        # utolsó chunk
        if current_chunk:
            chunks.append(" ".join(current_chunk))

        return chunks
    
    def create_chunks_structured(self, scene: list[dict]):

        chunks = []
        current_chunk = []

        for p in scene:

            text = p["text"]

            # -----------------------
            # SIMPLE RULE (v1)
            # -----------------------

            # ha heading → külön chunk
            if p.get("style", "").startswith("Heading"):
                if current_chunk:
                    chunks.append(self._merge(current_chunk))
                    current_chunk = []

                chunks.append({
                    "text": text,
                    "style": p.get("style", "Normal")
                })
                continue

            # normál bekezdés
            current_chunk.append(p)

        if current_chunk:
            chunks.append(self._merge(current_chunk))

        return chunks

    def _merge(self, paragraphs: list[dict]):

        text = "\n".join(p["text"] for p in paragraphs)

        # style öröklés (egyszerű szabály)
        style = paragraphs[0].get("style", "Normal")

        return {
            "text": text,
            "style": style
        }