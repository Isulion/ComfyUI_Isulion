from typing import Dict
from .base_handler import BaseThemeHandler
from .registry import register_theme

@register_theme("papercraft")
class PapercraftThemeHandler(BaseThemeHandler):
    def generate(self, custom_subject: str = "",
                 custom_location: str = "",
                 include_environment: bool = True,
                 include_style: bool = True,
                 include_effects: bool = True) -> Dict[str, str]:
        components = {}

        subject = self._get_random_choice("papercraft.subjects")
        material = self._get_random_choice("papercraft.materials")

        if custom_subject:
            components["subject"] = (
                f"((handcrafted papercraft)) of {custom_subject}, "
                f"((made from {material})), "
                f"((intricate paper construction))"
            )
        else:
            components["subject"] = (
                f"((handcrafted papercraft)) of (({subject})), "
                f"((made from {material})), "
                f"((intricate paper construction))"
            )

        if include_environment:
            if custom_location:
                components["environment"] = (
                    f"((displayed in {custom_location})), "
                    f"((diorama setting))"
                )
            else:
                env = self._get_random_choice("papercraft.environments")
                components["environment"] = (
                    f"((displayed in {env})), "
                    f"((diorama setting))"
                )

        if include_style:
            style = self._get_random_choice("papercraft.styles")
            lighting = self._get_random_choice("papercraft.lighting")
            components["style"] = (
                f"(({style})), "
                f"(({lighting})), "
                f"((macro detail)), precise craftsmanship"
            )

        if include_effects:
            effect = self._get_random_choice("papercraft.effects")
            mood = self._get_random_choice("papercraft.moods")
            components["effects"] = (
                f"with (({effect})), "
                f"(({mood} atmosphere))"
            )

        return components