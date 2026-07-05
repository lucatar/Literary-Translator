import re


class SceneSplitter:

    def split(self, text: str):
        lines = text.split("\n")

        scenes = []
        current_scene = []

        for line in lines:
            stripped = line.strip()

            # Chapter / scene break
            if self._is_scene_break(stripped):

                # Lezárjuk az előző scene-t
                if current_scene:
                    scenes.append("\n".join(current_scene).strip())

                # Új scene indul, aminek első sora maga a marker
                current_scene = [line]

                continue

            current_scene.append(line)

        # Utolsó scene
        if current_scene:
            scenes.append("\n".join(current_scene).strip())

        return scenes

    def _is_scene_break(self, stripped_line: str) -> bool:

        # Explicit scene separator
        if stripped_line == "***":
            return True

        # Chapter numbering (pl. "8.")
        if re.match(r"^\d+\.$", stripped_line):
            return True

        return False