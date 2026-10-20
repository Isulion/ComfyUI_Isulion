from typing import Dict
from .base_handler import BaseThemeHandler
from .registry import register_theme

@register_theme("psychedelic_cyber_fungus")
class PsychedelicCyberFungusThemeHandler(BaseThemeHandler):
    DISPLAY_NAME = "🍄 Psychedelic Cyber Fungus"
    def generate(self, custom_subject="", custom_location="",
                 include_environment=True, include_style=True, include_effects=True) -> Dict[str, str]:
        components = {}
        subject = self._get_random_choice("psychedelic_cyber_fungus.subjects")
        fungus = self._get_random_choice("psychedelic_cyber_fungus.fungus_types")
        if custom_subject:
            components["subject"] = f"((psychedelic cyber fungus)) (({custom_subject})), ((overgrown with {fungus})), ((bio-digital fusion))"
        else:
            components["subject"] = f"((psychedelic cyber fungus)) (({subject})), ((overgrown with {fungus})), ((bio-digital fusion))"
        if include_environment:
            env = self._get_random_choice("psychedelic_cyber_fungus.environments") if not custom_location else custom_location
            components["environment"] = f"((in {env})), ((fungal network))"
        if include_style:
            style = self._get_random_choice("psychedelic_cyber_fungus.style")
            components["style"] = f"(({style}))"
        if include_effects:
            effect = self._get_random_choice("psychedelic_cyber_fungus.effects")
            lighting = self._get_random_choice("psychedelic_cyber_fungus.lighting")
            mood = self._get_random_choice("psychedelic_cyber_fungus.moods")
            components["effects"] = f"(({effect})), (({lighting})), (({mood}))"
        return components
