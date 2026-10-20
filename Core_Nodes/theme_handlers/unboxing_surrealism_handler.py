from typing import Dict
from .base_handler import BaseThemeHandler
from .registry import register_theme

@register_theme("unboxing_surrealism")
class UnboxingSurrealismThemeHandler(BaseThemeHandler):
    DISPLAY_NAME = "📦 Unboxing Surrealism"
    def generate(self, custom_subject="", custom_location="",
                 include_environment=True, include_style=True, include_effects=True) -> Dict[str, str]:
        components = {}
        subject = self._get_random_choice("unboxing_surrealism.subjects")
        packaging = self._get_random_choice("unboxing_surrealism.packaging_styles")
        if custom_subject:
            components["subject"] = f"((unboxing surrealism)) (({custom_subject})), ((sealed in {packaging})), ((packaged fantasy))"
        else:
            components["subject"] = f"((unboxing surrealism)) (({subject})), ((sealed in {packaging})), ((packaged fantasy))"
        if include_environment:
            env = self._get_random_choice("unboxing_surrealism.environments") if not custom_location else custom_location
            components["environment"] = f"((in {env})), ((display box world))"
        if include_style:
            style = self._get_random_choice("unboxing_surrealism.style")
            components["style"] = f"(({style}))"
        if include_effects:
            effect = self._get_random_choice("unboxing_surrealism.effects")
            lighting = self._get_random_choice("unboxing_surrealism.lighting")
            mood = self._get_random_choice("unboxing_surrealism.moods")
            components["effects"] = f"(({effect})), (({lighting})), (({mood}))"
        return components
