from typing import Dict
from .base_handler import BaseThemeHandler
from .registry import register_theme

@register_theme("retro_vaporwave_mall")
class RetroVaporwaveMallThemeHandler(BaseThemeHandler):
    def generate(self, custom_subject="", custom_location="",
                 include_environment=True, include_style=True, include_effects=True) -> Dict[str, str]:
        components = {}
        subject = self._get_random_choice("retro_vaporwave_mall.subjects")
        element = self._get_random_choice("retro_vaporwave_mall.vaporwave_elements")
        if custom_subject:
            components["subject"] = f"((retro vaporwave mall)) (({custom_subject})), (({element})), ((abandoned 80s utopia))"
        else:
            components["subject"] = f"((retro vaporwave mall)) (({subject})), (({element})), ((abandoned 80s utopia))"
        if include_environment:
            env = self._get_random_choice("retro_vaporwave_mall.environments") if not custom_location else custom_location
            components["environment"] = f"((in {env})), ((permanent sunset mall))"
        if include_style:
            style = self._get_random_choice("retro_vaporwave_mall.style")
            components["style"] = f"(({style}))"
        if include_effects:
            effect = self._get_random_choice("retro_vaporwave_mall.effects")
            lighting = self._get_random_choice("retro_vaporwave_mall.lighting")
            mood = self._get_random_choice("retro_vaporwave_mall.moods")
            components["effects"] = f"(({effect})), (({lighting})), (({mood}))"
        return components