from typing import Dict
from .base_handler import BaseThemeHandler
from .registry import register_theme

@register_theme("cinematic_neon_rain")
class CinematicNeonRainThemeHandler(BaseThemeHandler):
    def generate(self, custom_subject: str = "",
                 custom_location: str = "",
                 include_environment: bool = True,
                 include_style: bool = True,
                 include_effects: bool = True) -> Dict[str, str]:
        components = {}

        subject = self._get_random_choice("cinematic_neon_rain.subjects")
        color = self._get_random_choice("cinematic_neon_rain.colors")

        if custom_subject:
            components["subject"] = (
                f"((cinematic neon rain shot)) of {custom_subject}, "
                f"(({color} color palette)), "
                f"((drenched in atmosphere))"
            )
        else:
            components["subject"] = (
                f"((cinematic neon rain shot)) of (({subject})), "
                f"(({color} color palette)), "
                f"((drenched in atmosphere))"
            )

        if include_environment:
            if custom_location:
                components["environment"] = (
                    f"((in {custom_location})), "
                    f"((wet reflective city night))"
                )
            else:
                env = self._get_random_choice("cinematic_neon_rain.environments")
                components["environment"] = (
                    f"((in {env})), "
                    f"((wet reflective city night))"
                )

        if include_style:
            style = self._get_random_choice("cinematic_neon_rain.styles")
            lighting = self._get_random_choice("cinematic_neon_rain.lighting")
            components["style"] = (
                f"(({style})), "
                f"(({lighting})), "
                f"((cinematic grade color grading))"
            )

        if include_effects:
            effect = self._get_random_choice("cinematic_neon_rain.effects")
            mood = self._get_random_choice("cinematic_neon_rain.moods")
            components["effects"] = (
                f"with (({effect})), "
                f"(({mood} atmosphere))"
            )

        return components