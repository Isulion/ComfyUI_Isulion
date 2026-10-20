from typing import Dict
from .base_handler import BaseThemeHandler
from .registry import register_theme

@register_theme("glitch_core")
class GlitchCoreThemeHandler(BaseThemeHandler):
    DISPLAY_NAME = "🌌 Glitch Core"
    def generate(self, custom_subject="", custom_location="",
                 include_environment=True, include_style=True, include_effects=True) -> Dict[str, str]:
        components = {}
        subject = self._get_random_choice("glitch_core.subjects")
        glitch = self._get_random_choice("glitch_core.glitch_types")
        if custom_subject:
            components["subject"] = f"((glitch core)) (({custom_subject})), (({glitch})), ((reality distortion))"
        else:
            components["subject"] = f"((glitch core)) (({subject})), (({glitch})), ((reality distortion))"
        if include_environment:
            env = self._get_random_choice("glitch_core.environments") if not custom_location else custom_location
            components["environment"] = f"((in {env})), ((broken simulation))"
        if include_style:
            style = self._get_random_choice("glitch_core.style")
            components["style"] = f"(({style}))"
        if include_effects:
            effect = self._get_random_choice("glitch_core.effects")
            lighting = self._get_random_choice("glitch_core.lighting")
            mood = self._get_random_choice("glitch_core.moods")
            components["effects"] = f"(({effect})), (({lighting})), (({mood}))"
        return components
