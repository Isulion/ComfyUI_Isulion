from typing import Dict
from .base_handler import BaseThemeHandler
from .registry import register_theme

@register_theme("cyber_hypebeast")
class CyberHypebeastThemeHandler(BaseThemeHandler):
    DISPLAY_NAME = "👟 Cyber Hypebeast"
    def generate(self, custom_subject="", custom_location="",
                 include_environment=True, include_style=True, include_effects=True) -> Dict[str, str]:
        components = {}
        subject = self._get_random_choice("cyber_hypebeast.subjects")
        brand = self._get_random_choice("cyber_hypebeast.streetwear_brands")
        if custom_subject:
            components["subject"] = f"((cyber hypebeast)) (({custom_subject})), ((wearing {brand})), ((mythological streetwear))"
        else:
            components["subject"] = f"((cyber hypebeast)) (({subject})), ((wearing {brand})), ((mythological streetwear))"
        if include_environment:
            env = self._get_random_choice("cyber_hypebeast.environments") if not custom_location else custom_location
            components["environment"] = f"((in {env})), ((cyber fashion district))"
        if include_style:
            style = self._get_random_choice("cyber_hypebeast.style")
            components["style"] = f"(({style}))"
        if include_effects:
            effect = self._get_random_choice("cyber_hypebeast.effects")
            lighting = self._get_random_choice("cyber_hypebeast.lighting")
            mood = self._get_random_choice("cyber_hypebeast.moods")
            components["effects"] = f"(({effect})), (({lighting})), (({mood}))"
        return components
