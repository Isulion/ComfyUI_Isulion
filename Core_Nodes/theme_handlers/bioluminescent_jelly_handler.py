from typing import Dict
from .base_handler import BaseThemeHandler
from .registry import register_theme

@register_theme("bioluminescent_jelly")
class BioluminescentJellyThemeHandler(BaseThemeHandler):
    def generate(self, custom_subject="", custom_location="",
                 include_environment=True, include_style=True, include_effects=True) -> Dict[str, str]:
        components = {}
        subject = self._get_random_choice("bioluminescent_jelly.subjects")
        structure = self._get_random_choice("bioluminescent_jelly.inner_structures")
        color = self._get_random_choice("bioluminescent_jelly.colors")
        if custom_subject:
            components["subject"] = f"((bioluminescent jelly)) (({custom_subject})), (({structure})), (({color} glow))"
        else:
            components["subject"] = f"((bioluminescent jelly)) (({subject})), (({structure})), (({color} glow))"
        if include_environment:
            env = self._get_random_choice("bioluminescent_jelly.environments") if not custom_location else custom_location
            components["environment"] = f"((in {env})), ((jellyfish dreamscape))"
        if include_style:
            style = self._get_random_choice("bioluminescent_jelly.style")
            components["style"] = f"(({style}))"
        if include_effects:
            effect = self._get_random_choice("bioluminescent_jelly.effects")
            lighting = self._get_random_choice("bioluminescent_jelly.lighting")
            mood = self._get_random_choice("bioluminescent_jelly.moods")
            components["effects"] = f"(({effect})), (({lighting})), (({mood}))"
        return components