import os
import glob

from src.parser import DocumentParser
from src.SceneSplitter import SceneSplitter
from src.chunker import Chunker

from src.analysis.cache_manager import AnalysisCacheManager
from src.analysis.POV_analyzer import POVAnalyzer
from src.analysis.style_builder import StyleBuilder
from src.analysis.glossary_builder import GlossaryBuilder

from src.translation.engine import TranslationEngine
from src.translation.translator import Translator
from src.translation.cache_manager import TranslationCacheManager

from src.export.docx_exporter import DocxExporter

from src.utils.file_writer import FileWriter
from src.post_process.build_overrides import build_translation_overrides
from src.post_process.apply_overrides import apply_translation_overrides


config = {
    "lang": "en",
    "chunk_size": 1200,
    "use_cache": True,
    "rebuild_analysis": False,
    "rebuild_translation": False
}


def run_pipeline(input_path: str, output_path: str):

    writer = FileWriter()

    # -------------------
    # 1. LOAD
    # -------------------

    parser = DocumentParser(input_path)
    paragraphs = parser.read()          # LIST[str]
    
    raw_text = "\n".join(paragraphs)    # STRING

    # -------------------
    # 2. SCENE SPLIT
    # -------------------

    scene_splitter = SceneSplitter()
    scenes = scene_splitter.split(raw_text)   # STRING IN / STRING OUT
    print("=== FIRST SCENE ===")
    print(repr(scenes[0][:500]))
    # -------------------
    # 3. CHUNKING
    # -------------------

    chunker = Chunker()
    chunks = []

    for scene in scenes:
        scene_chunks = chunker.create_chunks(scene)
        chunks.extend(scene_chunks)

    # -------------------
    # ANALYSIS CACHE
    # -------------------

    analysis_cache = AnalysisCacheManager(
        knowledge_base_dir="project/knowledge_base"
    )

    if config["rebuild_analysis"]:
        analysis_cache.rebuild()

    # -------------------
    # POV ANALYSIS
    # -------------------

    pov_analysis = analysis_cache.get_pov_analysis()

    if pov_analysis is None:
        pov_analyzer = POVAnalyzer()

        print("Analyzing POVs...")

        pov_analysis = pov_analyzer.analyze_chunks(chunks)

        analysis_cache.save_pov_analysis(pov_analysis)

    # -------------------
    # STYLE PROFILES
    # -------------------

    style_profiles = analysis_cache.get_style_profiles()

    if style_profiles is None:

        print("Building style profiles...")

        style_profiles = {}
        style_builder = StyleBuilder()

        reference_files_list = glob.glob(
            "input/reference_translation_*.docx"
        )

        reference_files = {}

        for path in reference_files_list:
            filename = os.path.basename(path)

            pov = filename.replace(
                "reference_translation_",
                ""
            ).replace(".docx", "")

            reference_files[pov] = path

        for pov, reference_path in reference_files.items():

            if not os.path.exists(reference_path):
                continue

            # NOTE: simplified (string-based)

            parser_ref = DocumentParser(reference_path)
            reference_translation = "\n".join(parser_ref.read())

            style_profiles[pov] = style_builder.build_style(
                source_text="\n".join(chunks),
                reference_translation=reference_translation
            )

            print(f"Built style profile for {pov}")

        analysis_cache.save_style_profiles(style_profiles)

    # -------------------
    # GLOSSARY
    # -------------------

    glossary = analysis_cache.get_glossary()

    if glossary is None:

        print("Building glossary...")

        glossary_builder = GlossaryBuilder()

        manuscript_text = "\n\n".join(chunks)

        glossary = glossary_builder.build_glossary(manuscript_text)

        analysis_cache.save_glossary(glossary)

    # -------------------
    # TRANSLATION
    # -------------------

    translator = Translator()

    translation_cache = TranslationCacheManager(
        project_dir="project",
        lang=config["lang"]
    )

    if config["rebuild_translation"]:
        translation_cache.rebuild()

    engine = TranslationEngine(
        translator,
        translation_cache,
        config
    )

    translated_chunks = engine.translate_document(
        chunks,
        style_profiles,
        pov_analysis,
        glossary
    )

    # -------------------
    # EXPORT
    # -------------------

    exporter = DocxExporter()
    exporter.add_chunks(translated_chunks)
    exporter.save(output_path)

# -------------------

    # 5. TRANSLATION OVERRIDES

    # -------------------

    build_translation_overrides(

        "project/knowledge_base"

    )



    apply_translation_overrides(

        output_path,

        "project/knowledge_base"

    )
    print("DONE 🚀")

    return analysis_cache


if __name__ == "__main__":

    analysis_cache = run_pipeline(
        input_path="input/manuscript.docx",
        output_path="output/translated.docx"
    )