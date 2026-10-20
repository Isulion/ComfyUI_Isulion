from typing import Dict
from .base_handler import BaseThemeHandler
from .registry import register_theme

@register_theme("inflatable_world")
class InflatableWorldThemeHandler(BaseThemeHandler):
    DISPLAY_NAME = "🎈 Inflatable World"
    def generate(self, custom_subject="", custom_location="",
                 include_environment=True, include_style=True, include_effects=True) -> Dict[str, str]:
        components = {}
        subject = self._get_random_choice("inflatable_world.subjects")
        material = self._get_random_choice("inflatable_world.materials")
        if custom_subject:
            components["subject"] = f"((inflatable world)) (({custom_subject})), ((made of {material})), ((balloon inflation detail))"
        else:
            components["subject"] = f"((inflatable world)) (({subject})), ((made of {material})), ((balloon inflation detail))"
        if include_environment:
            env = self._get_random_choice("inflatable_world.environments") if not custom_location else custom_location
            components["environment"] = f"((in {env})), ((inflatable landscape))"
        if include_style:
            style = self._get_random_choice("inflatable_world.style")
            components["style"] = f"(({style}))"
        if include_effects:
            effect = self._get_random_choice("inflatable_world.effects")
            lighting = self._get_random_choice("inflatable_world.lighting")
            mood = self._get_random_choice("inflatable_world.moods")
            components["effects"] = f"(({effect})), (({lighting})), (({mood}))"
        return components
