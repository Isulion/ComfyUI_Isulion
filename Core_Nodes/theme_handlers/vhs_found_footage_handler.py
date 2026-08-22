from typing import Dict
from .base_handler import BaseThemeHandler
from .registry import register_theme

@register_theme("vhs_found_footage")
class VHSFoundFootageThemeHandler(BaseThemeHandler):
    def generate(self, custom_subject="", custom_location="",
                 include_environment=True, include_style=True, include_effects=True) -> Dict[str, str]:
        components = {}
        subject = self._get_random_choice("vhs_found_footage.subjects")
        artifact = self._get_random_choice("vhs_found_footage.tape_artifacts")
        if custom_subject:
            components["subject"] = f"((VHS found footage)) (({custom_subject})), (({artifact})), ((analog horror tape))"
        else:
            components["subject"] = f"((VHS found footage)) (({subject})), (({artifact})), ((analog horror tape))"
        if include_environment:
            env = self._get_random_choice("vhs_found_footage.environments") if not custom_location else custom_location
            components["environment"] = f"((recorded in {env})), ((found footage location))"
        if include_style:
            style = self._get_random_choice("vhs_found_footage.style")
            components["style"] = f"(({style}))"
        if include_effects:
            effect = self._get_random_choice("vhs_found_footage.effects")
            lighting = self._get_random_choice("vhs_found_footage.lighting")
            mood = self._get_random_choice("vhs_found_footage.moods")
            components["effects"] = f"(({effect})), (({lighting})), (({mood}))"
        return components