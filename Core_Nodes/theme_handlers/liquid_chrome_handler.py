from typing import Dict
from .base_handler import BaseThemeHandler
from .registry import register_theme

@register_theme("liquid_chrome")
class LiquidChromeThemeHandler(BaseThemeHandler):
    def generate(self, custom_subject="", custom_location="",
                 include_environment=True, include_style=True, include_effects=True) -> Dict[str, str]:
        components = {}
        subject = self._get_random_choice("liquid_chrome.subjects")
        fluid = self._get_random_choice("liquid_chrome.fluid_states")
        if custom_subject:
            components["subject"] = f"((liquid chrome)) (({custom_subject})), (({fluid})), ((molten metal flow))"
        else:
            components["subject"] = f"((liquid chrome)) (({subject})), (({fluid})), ((molten metal flow))"
        if include_environment:
            env = self._get_random_choice("liquid_chrome.environments") if not custom_location else custom_location
            components["environment"] = f"((in {env})), ((mercury world))"
        if include_style:
            style = self._get_random_choice("liquid_chrome.style")
            components["style"] = f"(({style})), ((liquid metal perfection))"
        if include_effects:
            effect = self._get_random_choice("liquid_chrome.effects")
            lighting = self._get_random_choice("liquid_chrome.lighting")
            mood = self._get_random_choice("liquid_chrome.moods")
            components["effects"] = f"(({effect})), (({lighting})), (({mood}))"
        return components