from typing import Dict
from .base_handler import BaseThemeHandler
from .registry import register_theme

@register_theme("giant_cat_zilla")
class GiantCatZillaThemeHandler(BaseThemeHandler):
    def generate(self, custom_subject="", custom_location="",
                 include_environment=True, include_style=True, include_effects=True) -> Dict[str, str]:
        components = {}
        subject = self._get_random_choice("giant_cat_zilla.subjects")
        destruction = self._get_random_choice("giant_cat_zilla.destruction_styles")
        if custom_subject:
            components["subject"] = f"((giant cat-zilla kaiju)) (({custom_subject})), (({destruction})), ((catastrophic feline rampage))"
        else:
            components["subject"] = f"((giant cat-zilla)) (({subject})), (({destruction})), ((catastrophic feline rampage))"
        if include_environment:
            env = self._get_random_choice("giant_cat_zilla.environments") if not custom_location else custom_location
            components["environment"] = f"((destroying {env})), ((city in chaos))"
        if include_style:
            style = self._get_random_choice("giant_cat_zilla.style")
            lighting = self._get_random_choice("giant_cat_zilla.lighting")
            components["style"] = f"(({style})), (({lighting}))"
        if include_effects:
            effect = self._get_random_choice("giant_cat_zilla.effects")
            mood = self._get_random_choice("giant_cat_zilla.moods")
            components["effects"] = f"(({effect})), (({mood}))"
        return components