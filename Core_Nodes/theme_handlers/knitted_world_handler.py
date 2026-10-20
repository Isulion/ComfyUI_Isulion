from typing import Dict
from .base_handler import BaseThemeHandler
from .registry import register_theme

@register_theme("knitted_world")
class KnittedWorldThemeHandler(BaseThemeHandler):
    DISPLAY_NAME = "🧶 Knitted World"
    def generate(self, custom_subject="", custom_location="",
                 include_environment=True, include_style=True, include_effects=True) -> Dict[str, str]:
        components = {}
        subject = self._get_random_choice("knitted_world.subjects")
        stitch = self._get_random_choice("knitted_world.stitch_types")
        if custom_subject:
            components["subject"] = f"((knitted world)) (({custom_subject})), (({stitch} texture)), ((yarn craft detail))"
        else:
            components["subject"] = f"((knitted world)) (({subject})), (({stitch} texture)), ((yarn craft detail))"
        if include_environment:
            env = self._get_random_choice("knitted_world.environments") if not custom_location else custom_location
            components["environment"] = f"((in {env})), ((yarn landscape))"
        if include_style:
            style = self._get_random_choice("knitted_world.style")
            components["style"] = f"(({style}))"
        if include_effects:
            effect = self._get_random_choice("knitted_world.effects")
            lighting = self._get_random_choice("knitted_world.lighting")
            mood = self._get_random_choice("knitted_world.moods")
            components["effects"] = f"(({effect})), (({lighting})), (({mood}))"
        return components
