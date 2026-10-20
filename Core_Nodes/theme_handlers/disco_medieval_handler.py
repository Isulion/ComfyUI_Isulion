from typing import Dict
from .base_handler import BaseThemeHandler
from .registry import register_theme

@register_theme("disco_medieval")
class DiscoMedievalThemeHandler(BaseThemeHandler):
    DISPLAY_NAME = "🪩 Disco Medieval"
    def generate(self, custom_subject="", custom_location="",
                 include_environment=True, include_style=True, include_effects=True) -> Dict[str, str]:
        components = {}
        subject = self._get_random_choice("disco_medieval.subjects")
        weapon = self._get_random_choice("disco_medieval.weapons")
        if custom_subject:
            components["subject"] = f"((disco medieval)) (({custom_subject})), ((wielding {weapon})), ((80s fantasy nightclub))"
        else:
            components["subject"] = f"((disco medieval)) (({subject})), ((wielding {weapon})), ((80s fantasy nightclub))"
        if include_environment:
            env = self._get_random_choice("disco_medieval.environments") if not custom_location else custom_location
            components["environment"] = f"((in {env})), ((medieval rave))"
        if include_style:
            style = self._get_random_choice("disco_medieval.style")
            components["style"] = f"(({style})), ((disco fever dream))"
        if include_effects:
            lighting = self._get_random_choice("disco_medieval.lighting")
            effect = self._get_random_choice("disco_medieval.effects")
            mood = self._get_random_choice("disco_medieval.moods")
            components["effects"] = f"(({lighting})), (({effect})), (({mood}))"
        return components
