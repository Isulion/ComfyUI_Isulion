from typing import Dict
from .base_handler import BaseThemeHandler
from .registry import register_theme

@register_theme("rubber_duck")
class RubberDuckThemeHandler(BaseThemeHandler):
    DISPLAY_NAME = "🦆 Rubber Duck Supremacy"
    def generate(self, custom_subject="", custom_location="",
                 include_environment=True, include_style=True, include_effects=True) -> Dict[str, str]:
        components = {}
        subject = self._get_random_choice("rubber_duck.subjects")
        accessory = self._get_random_choice("rubber_duck.duck_accessories")
        if custom_subject:
            components["subject"] = f"((rubber duck supremacy)) (({custom_subject})), ((wearing {accessory})), ((sacred duck icon))"
        else:
            components["subject"] = f"((rubber duck supremacy)) (({subject})), ((wearing {accessory})), ((sacred duck icon))"
        if include_environment:
            env = self._get_random_choice("rubber_duck.environments") if not custom_location else custom_location
            components["environment"] = f"((in {env})), ((duck civilization))"
        if include_style:
            style = self._get_random_choice("rubber_duck.style")
            components["style"] = f"(({style}))"
        if include_effects:
            effect = self._get_random_choice("rubber_duck.effects")
            lighting = self._get_random_choice("rubber_duck.lighting")
            mood = self._get_random_choice("rubber_duck.moods")
            components["effects"] = f"(({effect})), (({lighting})), (({mood}))"
        return components
