from typing import Dict
from .base_handler import BaseThemeHandler
from .registry import register_theme

@register_theme("overgrown_ruins")
class OvergrownRuinsThemeHandler(BaseThemeHandler):
    DISPLAY_NAME = "🌿 Overgrown Ruins"
    def generate(self, custom_subject: str = "",
                 custom_location: str = "",
                 include_environment: bool = True,
                 include_style: bool = True,
                 include_effects: bool = True) -> Dict[str, str]:
        components = {}

        subject = self._get_random_choice("overgrown_ruins.subjects")
        flora = self._get_random_choice("overgrown_ruins.flora")

        if custom_subject:
            components["subject"] = (
                f"((overgrown ruin)) with {custom_subject}, "
                f"((covered in {flora})), "
                f"((nature reclaiming structure))"
            )
        else:
            components["subject"] = (
                f"((overgrown ruin)) of (({subject})), "
                f"((covered in {flora})), "
                f"((nature reclaiming structure))"
            )

        if include_environment:
            if custom_location:
                components["environment"] = (
                    f"((in {custom_location})), "
                    f"((wild reclaimed landscape))"
                )
            else:
                env = self._get_random_choice("overgrown_ruins.environments")
                components["environment"] = (
                    f"((in {env})), "
                    f"((wild reclaimed landscape))"
                )

        if include_style:
            style = self._get_random_choice("overgrown_ruins.styles")
            lighting = self._get_random_choice("overgrown_ruins.lighting")
            components["style"] = (
                f"(({style})), "
                f"(({lighting})), "
                f"((atmospheric natural reclamation))"
            )

        if include_effects:
            effect = self._get_random_choice("overgrown_ruins.effects")
            mood = self._get_random_choice("overgrown_ruins.moods")
            components["effects"] = (
                f"with (({effect})), "
                f"(({mood} atmosphere))"
            )

        return components
