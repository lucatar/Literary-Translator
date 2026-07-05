import os
import json


class AnalysisCacheManager:

    def __init__(self, knowledge_base_dir):

        self.knowledge_base_dir = knowledge_base_dir

        os.makedirs(self.knowledge_base_dir, exist_ok=True)

        self.pov_path = os.path.join(
            self.knowledge_base_dir,
            "pov_analysis.json"
        )

        self.style_path = os.path.join(
            self.knowledge_base_dir,
            "style_profiles.json"
        )

        self.glossary_path = os.path.join(
            self.knowledge_base_dir,
            "glossary.json"
        )


    # -------------------
    # Generic JSON helpers
    # -------------------

    def _load_json(self, path):

        if not os.path.exists(path):
            return None

        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)


    def _save_json(self, path, data):

        with open(path, "w", encoding="utf-8") as f:
            json.dump(
                data,
                f,
                ensure_ascii=False,
                indent=2
            )


    # -------------------
    # POV Analysis
    # -------------------

    def get_pov_analysis(self):
        return self._load_json(self.pov_path)


    def save_pov_analysis(self, analysis):
        self._save_json(self.pov_path, analysis)


    # -------------------
    # Style Profiles
    # -------------------

    def get_style_profiles(self):
        return self._load_json(self.style_path)


    def save_style_profiles(self, style_profiles):
        self._save_json(self.style_path, style_profiles)


    # -------------------
    # Glossary
    # -------------------

    def get_glossary(self):
        return self._load_json(self.glossary_path)


    def save_glossary(self, glossary):
        self._save_json(self.glossary_path, glossary)


    # -------------------
    # Rebuild
    # -------------------

    def rebuild(self):

        for path in [
            self.pov_path,
            self.style_path,
            self.glossary_path
        ]:

            if os.path.exists(path):
                os.remove(path)