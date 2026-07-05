import json
import os


def build_translation_overrides(knowledge_base_dir):

    glossary_path = os.path.join(
        knowledge_base_dir,
        "glossary.json"
    )

    overrides_path = os.path.join(
        knowledge_base_dir,
        "translation_overrides.json"
    )

    if os.path.exists(overrides_path):
        return

    with open(glossary_path, "r", encoding="utf-8") as f:
        glossary = json.load(f)

    overrides = {}

    for english in glossary["terms"].values():
        overrides[english] = english

    with open(overrides_path, "w", encoding="utf-8") as f:
        json.dump(
            overrides,
            f,
            ensure_ascii=False,
            indent=2
        )

    print("Created translation_overrides.json")