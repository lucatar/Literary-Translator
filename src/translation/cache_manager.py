import os
import json
import shutil


class TranslationCacheManager:

    def __init__(self, project_dir, lang):
        self.base = os.path.join(project_dir, "translations", lang)
        os.makedirs(self.base, exist_ok=True)

    def get_translated_chunk(self, idx):
        path = os.path.join(self.base, f"chunk_{idx}.json")

        if not os.path.exists(path):
            return None

        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)

    def save_translated_chunk(self, idx, data):
        path = os.path.join(self.base, f"chunk_{idx}.json")

        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)