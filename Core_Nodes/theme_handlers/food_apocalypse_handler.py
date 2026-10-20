from typing import Dict
from .base_handler import BaseThemeHandler
from .registry import register_theme

@register_theme("food_apocalypse")
class FoodApocalypseThemeHandler(BaseThemeHandler):
    DISPLAY_NAME = "🍕 Food Apocalypse"
    def generate(self, custom_subject="", custom_location="",
                 include_environment=True, include_style=True, include_effects=True) -> Dict[str, str]:
        components = {}
        subject = self._get_random_choice("food_apocalypse.subjects")
        disaster = self._get_random_choice("food_apocalypse.food_disasters")
        if custom_subject:
            components["subject"] = f"((food apocalypse)) (({custom_subject})), (({disaster})), ((junk food world))"
        else:
            components["subject"] = f"((food apocalypse)) (({subject})), (({disaster})), ((junk food world))"
        if include_environment:
            env = self._get_random_choice("food_apocalypse.environments") if not custom_location else custom_location
            components["environment"] = f"((in {env})), ((food wasteland))"
        if include_style:
            style = self._get_random_choice("food_apocalypse.style")
            components["style"] = f"(({style}))"
        if include_effects:
            effect = self._get_random_choice("food_apocalypse.effects")
            mood = self._get_random_choice("food_apocalypse.moods")
            components["effects"] = f"(({effect})), (({mood}))"
        return components
