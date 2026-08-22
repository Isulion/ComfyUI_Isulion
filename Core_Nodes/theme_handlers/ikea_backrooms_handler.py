from typing import Dict
from .base_handler import BaseThemeHandler
from .registry import register_theme

@register_theme("ikea_backrooms")
class IKEABackroomsThemeHandler(BaseThemeHandler):
    def generate(self, custom_subject="", custom_location="",
                 include_environment=True, include_style=True, include_effects=True) -> Dict[str, str]:
        components = {}
        subject = self._get_random_choice("ikea_backrooms.subjects")
        feature = self._get_random_choice("ikea_backrooms.liminal_features")
        if custom_subject:
            components["subject"] = f"((IKEA backrooms)) (({custom_subject})), (({feature})), ((liminal space))"
        else:
            components["subject"] = f"((IKEA backrooms)) (({subject})), (({feature})), ((liminal space))"
        if include_environment:
            env = self._get_random_choice("ikea_backrooms.environments") if not custom_location else custom_location
            components["environment"] = f"((in {env})), ((infinite showroom))"
        if include_style:
            style = self._get_random_choice("ikea_backrooms.style")
            components["style"] = f"(({style})), ((analog liminal horror))"
        if include_effects:
            effect = self._get_random_choice("ikea_backrooms.effects")
            lighting = self._get_random_choice("ikea_backrooms.lighting")
            mood = self._get_random_choice("ikea_backrooms.moods")
            components["effects"] = f"(({effect})), (({lighting})), (({mood}))"
        return components